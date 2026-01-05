"""
Admin Dashboard Routes
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from app.models import db, User, NewCar, UsedCar, Valuation, RecommendationHistory
from app import limiter, csrf
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper


# ==================== DASHBOARD ====================

@admin_bp.route('/')
def dashboard():
    """Admin dashboard home page"""
    # Get statistics
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'total_new_cars': NewCar.query.count(),
        'total_used_cars': UsedCar.query.count(),
        'available_used_cars': UsedCar.query.filter_by(is_sold=False).count(),
        'total_valuations': Valuation.query.count(),
        'pending_valuations': Valuation.query.filter_by(status='pending').count(),
    }

    # Recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_listings = UsedCar.query.order_by(UsedCar.listing_date.desc()).limit(5).all()
    recent_valuations = Valuation.query.order_by(Valuation.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_users=recent_users,
                         recent_listings=recent_listings,
                         recent_valuations=recent_valuations)


# ==================== USER MANAGEMENT ====================

@admin_bp.route('/users')
def users_list():
    """List all users"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')

    query = User.query

    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )

    if role_filter:
        query = query.filter_by(role=role_filter)

    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('admin/users.html',
                         users=pagination.items,
                         pagination=pagination,
                         search=search,
                         role_filter=role_filter)


@admin_bp.route('/users/<int:user_id>')
def user_detail(user_id):
    """View user details"""
    user = User.query.get_or_404(user_id)
    valuations = Valuation.query.filter_by(user_id=user_id).order_by(Valuation.created_at.desc()).limit(10).all()
    recommendations = RecommendationHistory.query.filter_by(user_id=user_id).order_by(RecommendationHistory.created_at.desc()).limit(10).all()

    return render_template('admin/user_detail.html',
                         user=user,
                         valuations=valuations,
                         recommendations=recommendations)


@admin_bp.route('/api/users/<int:user_id>/toggle-active', methods=['POST'])
@csrf.exempt
@admin_required
def toggle_user_active(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)

    # Prevent deactivating yourself
    if str(user.id) == get_jwt_identity():
        return jsonify({'error': 'Cannot deactivate your own account'}), 400

    user.is_active = not user.is_active
    db.session.commit()

    return jsonify({
        'success': True,
        'is_active': user.is_active,
        'message': f'User {"activated" if user.is_active else "deactivated"} successfully'
    })


@admin_bp.route('/api/users/<int:user_id>/change-role', methods=['POST'])
@csrf.exempt
@admin_required
def change_user_role(user_id):
    """Change user role"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    new_role = data.get('role')

    if new_role not in ['user', 'admin', 'moderator']:
        return jsonify({'error': 'Invalid role'}), 400

    user.role = new_role
    db.session.commit()

    return jsonify({
        'success': True,
        'role': user.role,
        'message': f'User role changed to {new_role}'
    })


# ==================== CAR MANAGEMENT ====================

@admin_bp.route('/cars')
def cars_list():
    """List all used cars"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    search = request.args.get('search', '')
    status = request.args.get('status', '')

    query = UsedCar.query

    if search:
        query = query.filter(
            (UsedCar.brand.ilike(f'%{search}%')) |
            (UsedCar.model.ilike(f'%{search}%')) |
            (UsedCar.seller_name.ilike(f'%{search}%'))
        )

    if status == 'available':
        query = query.filter_by(is_sold=False)
    elif status == 'sold':
        query = query.filter_by(is_sold=True)

    pagination = query.order_by(UsedCar.listing_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('admin/cars.html',
                         cars=pagination.items,
                         pagination=pagination,
                         search=search,
                         status=status)


@admin_bp.route('/cars/<int:listing_id>')
def car_detail(listing_id):
    """View car details"""
    car = UsedCar.query.filter_by(listing_id=listing_id).first_or_404()
    return render_template('admin/car_detail.html', car=car)


@admin_bp.route('/api/cars/<int:listing_id>/toggle-sold', methods=['POST'])
@csrf.exempt
@admin_required
def toggle_car_sold(listing_id):
    """Toggle car sold status"""
    car = UsedCar.query.filter_by(listing_id=listing_id).first_or_404()
    car.is_sold = not car.is_sold
    db.session.commit()

    return jsonify({
        'success': True,
        'is_sold': car.is_sold,
        'message': f'Car marked as {"sold" if car.is_sold else "available"}'
    })


@admin_bp.route('/api/cars/<int:listing_id>', methods=['DELETE'])
@csrf.exempt
@admin_required
def delete_car(listing_id):
    """Delete a car listing"""
    car = UsedCar.query.filter_by(listing_id=listing_id).first_or_404()
    db.session.delete(car)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Car listing deleted successfully'
    })


# ==================== VALUATION MANAGEMENT ====================

@admin_bp.route('/valuations')
def valuations_list():
    """List all valuations"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    status = request.args.get('status', '')

    query = Valuation.query

    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Valuation.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('admin/valuations.html',
                         valuations=pagination.items,
                         pagination=pagination,
                         status=status)


@admin_bp.route('/valuations/<int:valuation_id>')
def valuation_detail(valuation_id):
    """View valuation details"""
    valuation = Valuation.query.get_or_404(valuation_id)
    return render_template('admin/valuation_detail.html', valuation=valuation)


@admin_bp.route('/api/valuations/<int:valuation_id>/status', methods=['POST'])
@csrf.exempt
@admin_required
def update_valuation_status(valuation_id):
    """Update valuation status"""
    valuation = Valuation.query.get_or_404(valuation_id)
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['pending', 'reviewed', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400

    valuation.status = new_status
    db.session.commit()

    return jsonify({
        'success': True,
        'status': valuation.status,
        'message': f'Valuation status updated to {new_status}'
    })


# ==================== ANALYTICS ====================

@admin_bp.route('/analytics')
def analytics():
    """Analytics dashboard"""
    # Get date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Daily registrations (last 30 days)
    daily_users = db.session.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= start_date
    ).group_by(
        func.date(User.created_at)
    ).all()

    # Daily valuations (last 30 days)
    daily_valuations = db.session.query(
        func.date(Valuation.created_at).label('date'),
        func.count(Valuation.id).label('count')
    ).filter(
        Valuation.created_at >= start_date
    ).group_by(
        func.date(Valuation.created_at)
    ).all()

    # Top brands by listings
    top_brands = db.session.query(
        UsedCar.brand,
        func.count(UsedCar.id).label('count')
    ).group_by(UsedCar.brand).order_by(func.count(UsedCar.id).desc()).limit(10).all()

    # Price distribution
    price_ranges = [
        ('Under 3L', 0, 300000),
        ('3L - 5L', 300000, 500000),
        ('5L - 10L', 500000, 1000000),
        ('10L - 20L', 1000000, 2000000),
        ('Above 20L', 2000000, 100000000)
    ]

    price_distribution = []
    for label, min_price, max_price in price_ranges:
        count = UsedCar.query.filter(
            UsedCar.current_price >= min_price,
            UsedCar.current_price < max_price
        ).count()
        price_distribution.append({'label': label, 'count': count})

    return render_template('admin/analytics.html',
                         daily_users=daily_users,
                         daily_valuations=daily_valuations,
                         top_brands=top_brands,
                         price_distribution=price_distribution)


# ==================== API STATS ====================

@admin_bp.route('/api/stats')
@csrf.exempt
@admin_required
def api_stats():
    """Get dashboard statistics as JSON"""
    stats = {
        'users': {
            'total': User.query.count(),
            'active': User.query.filter_by(is_active=True).count(),
            'admins': User.query.filter_by(role='admin').count()
        },
        'cars': {
            'new_cars': NewCar.query.count(),
            'used_cars_total': UsedCar.query.count(),
            'used_cars_available': UsedCar.query.filter_by(is_sold=False).count(),
            'used_cars_sold': UsedCar.query.filter_by(is_sold=True).count()
        },
        'valuations': {
            'total': Valuation.query.count(),
            'pending': Valuation.query.filter_by(status='pending').count(),
            'completed': Valuation.query.filter_by(status='completed').count()
        }
    }
    return jsonify(stats)
