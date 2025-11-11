"""
Flask routes for the Indian Automotive Marketplace
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app.models import db, NewCar, UsedCar, Valuation, RecommendationHistory
from utils.ml_helper import RecommendationEngine, PricePredictor, BuyBackValuator
import json
from datetime import datetime

main_bp = Blueprint('main', __name__)

# Initialize ML helpers
recommendation_engine = None
price_predictor = None
buyback_valuator = None

def init_ml_models():
    """Initialize ML models on first request"""
    global recommendation_engine, price_predictor, buyback_valuator
    if recommendation_engine is None:
        recommendation_engine = RecommendationEngine()
    if price_predictor is None:
        price_predictor = PricePredictor()
    if buyback_valuator is None:
        buyback_valuator = BuyBackValuator()


@main_bp.route('/')
def index():
    """Home page"""
    # Get some statistics
    total_new_cars = NewCar.query.count()
    total_used_cars = UsedCar.query.filter_by(is_sold=False).count()
    total_valuations = Valuation.query.count()

    # Get featured cars
    featured_new_cars = NewCar.query.order_by(NewCar.safety_rating.desc()).limit(6).all()
    featured_used_cars = UsedCar.query.filter_by(is_sold=False).order_by(
        UsedCar.condition_score.desc()).limit(6).all()

    return render_template('index.html',
                         total_new_cars=total_new_cars,
                         total_used_cars=total_used_cars,
                         total_valuations=total_valuations,
                         featured_new_cars=featured_new_cars,
                         featured_used_cars=featured_used_cars)


# ==================== NEW CAR RECOMMENDATION ROUTES ====================

@main_bp.route('/recommendations')
def recommendations():
    """New car recommendations page"""
    return render_template('recommendations/form.html')


@main_bp.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """API endpoint to get car recommendations"""
    init_ml_models()

    try:
        data = request.get_json()

        # Extract user preferences
        preferences = {
            'budget_min': int(data.get('budget_min', 500000)),
            'budget_max': int(data.get('budget_max', 1500000)),
            'fuel_type': data.get('fuel_type'),
            'body_type': data.get('body_type'),
            'transmission': data.get('transmission'),
            'usage_type': data.get('usage_type', 'mixed'),
            'family_size': int(data.get('family_size', 4)),
            'priority_factor': data.get('priority_factor', 'overall')
        }

        # Get recommendations from ML model
        recommendations = recommendation_engine.get_recommendations(preferences, top_n=5)

        # Save to history (optional - would need user_id)
        # history = RecommendationHistory(...)
        # db.session.add(history)
        # db.session.commit()

        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'preferences': preferences
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@main_bp.route('/recommendations/compare')
def compare_cars():
    """Compare multiple cars"""
    car_ids = request.args.getlist('car_ids')

    if not car_ids or len(car_ids) < 2:
        flash('Please select at least 2 cars to compare', 'warning')
        return redirect(url_for('main.recommendations'))

    cars = []
    for car_id in car_ids[:3]:  # Maximum 3 cars
        car = NewCar.query.filter_by(car_id=int(car_id)).first()
        if car:
            cars.append(car)

    return render_template('recommendations/compare.html', cars=cars)


# ==================== MARKETPLACE ROUTES ====================

@main_bp.route('/marketplace')
def marketplace():
    """Used cars marketplace listing page"""
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Filters
    brand = request.args.get('brand')
    body_type = request.args.get('body_type')
    fuel_type = request.args.get('fuel_type')
    transmission = request.args.get('transmission')
    price_min = request.args.get('price_min', type=int)
    price_max = request.args.get('price_max', type=int)
    year_min = request.args.get('year_min', type=int)

    # Build query
    query = UsedCar.query.filter_by(is_sold=False)

    if brand:
        query = query.filter(UsedCar.brand == brand)
    if body_type:
        query = query.filter(UsedCar.body_type == body_type)
    if fuel_type:
        query = query.filter(UsedCar.fuel_type == fuel_type)
    if transmission:
        query = query.filter(UsedCar.transmission == transmission)
    if price_min:
        query = query.filter(UsedCar.current_price >= price_min)
    if price_max:
        query = query.filter(UsedCar.current_price <= price_max)
    if year_min:
        query = query.filter(UsedCar.registration_year >= year_min)

    # Pagination
    pagination = query.order_by(UsedCar.listing_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    cars = pagination.items

    # Get unique values for filters
    brands = db.session.query(UsedCar.brand).distinct().all()
    brands = [b[0] for b in brands]

    body_types = db.session.query(UsedCar.body_type).distinct().all()
    body_types = [b[0] for b in body_types]

    return render_template('marketplace/listings.html',
                         cars=cars,
                         pagination=pagination,
                         brands=brands,
                         body_types=body_types)


@main_bp.route('/marketplace/car/<int:listing_id>')
def car_details(listing_id):
    """Car details page"""
    car = UsedCar.query.filter_by(listing_id=listing_id).first_or_404()

    # Get similar cars
    similar_cars = UsedCar.query.filter(
        UsedCar.listing_id != listing_id,
        UsedCar.brand == car.brand,
        UsedCar.is_sold == False
    ).limit(4).all()

    return render_template('marketplace/details.html',
                         car=car,
                         similar_cars=similar_cars)


@main_bp.route('/marketplace/list', methods=['GET', 'POST'])
def list_car():
    """List a car for sale"""
    if request.method == 'POST':
        try:
            # Get form data
            listing = UsedCar(
                listing_id=UsedCar.query.count() + 1001,  # Generate unique ID
                brand=request.form.get('brand'),
                model=request.form.get('model'),
                variant=request.form.get('variant'),
                body_type=request.form.get('body_type'),
                registration_year=int(request.form.get('registration_year')),
                age_years=2025 - int(request.form.get('registration_year')),
                fuel_type=request.form.get('fuel_type'),
                transmission=request.form.get('transmission'),
                mileage_km=int(request.form.get('mileage_km')),
                num_owners=int(request.form.get('num_owners')),
                original_price=int(request.form.get('original_price')),
                current_price=int(request.form.get('current_price')),
                condition_score=float(request.form.get('condition_score', 70)),
                insurance_validity_months=int(request.form.get('insurance_validity_months', 0)),
                service_history=request.form.get('service_history'),
                accident_history=request.form.get('accident_history'),
                color=request.form.get('color'),
                seating_capacity=int(request.form.get('seating_capacity', 5)),
                engine_cc=int(request.form.get('engine_cc', 1200)),
                fuel_efficiency_kmpl=float(request.form.get('fuel_efficiency_kmpl', 15)),
                rto=request.form.get('rto'),
                city=request.form.get('city'),
                features=request.form.get('features'),
                seller_name=request.form.get('seller_name'),
                seller_phone=request.form.get('seller_phone'),
                listing_date=datetime.now().date(),
                negotiable=request.form.get('negotiable', 'No'),
                test_drive_available=request.form.get('test_drive_available', 'Yes'),
                is_sold=False
            )

            db.session.add(listing)
            db.session.commit()

            flash('Your car has been listed successfully!', 'success')
            return redirect(url_for('main.car_details', listing_id=listing.listing_id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error listing car: {str(e)}', 'danger')

    return render_template('marketplace/list_car.html')


@main_bp.route('/api/predict-price', methods=['POST'])
def predict_price():
    """API endpoint to predict used car price"""
    init_ml_models()

    try:
        data = request.get_json()

        # Use price predictor
        predicted_price = price_predictor.predict_price(data)

        return jsonify({
            'success': True,
            'predicted_price': int(predicted_price)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# ==================== BUY-BACK VALUATION ROUTES ====================

@main_bp.route('/buyback')
def buyback():
    """Buy-back valuation page"""
    return render_template('buyback/form.html')


@main_bp.route('/api/buyback-valuation', methods=['POST'])
def buyback_valuation():
    """API endpoint for buy-back valuation"""
    init_ml_models()

    try:
        data = request.get_json()

        # Get valuation
        valuation_result = buyback_valuator.get_valuation(data)

        # Save valuation to database
        valuation = Valuation(
            brand=data.get('brand'),
            model=data.get('model'),
            variant=data.get('variant'),
            registration_year=int(data.get('registration_year')),
            mileage_km=int(data.get('mileage_km')),
            num_owners=int(data.get('num_owners')),
            fuel_type=data.get('fuel_type'),
            transmission=data.get('transmission'),
            service_history=data.get('service_history'),
            accident_history=data.get('accident_history'),
            insurance_valid=data.get('insurance_valid', False),
            modifications=data.get('modifications', ''),
            condition_score=valuation_result['condition_score'],
            estimated_price_min=valuation_result['estimated_price_min'],
            estimated_price_max=valuation_result['estimated_price_max'],
            estimated_price_avg=valuation_result['estimated_price_avg'],
            confidence_score=valuation_result['confidence_score'],
            customer_name=data.get('customer_name'),
            customer_phone=data.get('customer_phone'),
            customer_email=data.get('customer_email'),
            inspection_requested=data.get('inspection_requested', False),
            status='pending'
        )

        db.session.add(valuation)
        db.session.commit()

        valuation_result['valuation_id'] = valuation.id

        return jsonify({
            'success': True,
            'valuation': valuation_result
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@main_bp.route('/buyback/valuation/<int:valuation_id>')
def valuation_details(valuation_id):
    """Valuation details page"""
    valuation = Valuation.query.get_or_404(valuation_id)
    return render_template('buyback/valuation_details.html', valuation=valuation)


# ==================== UTILITY ROUTES ====================

@main_bp.route('/api/brands')
def get_brands():
    """Get list of brands"""
    brands = db.session.query(NewCar.brand).distinct().order_by(NewCar.brand).all()
    return jsonify([b[0] for b in brands])


@main_bp.route('/api/models/<brand>')
def get_models(brand):
    """Get models for a brand"""
    models = db.session.query(NewCar.model).filter_by(brand=brand).distinct().order_by(NewCar.model).all()
    return jsonify([m[0] for m in models])


@main_bp.route('/emi-calculator')
def emi_calculator():
    return render_template('emi_calculator.html')


# Error handlers
@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@main_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
