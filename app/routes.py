"""
Flask routes for the Indian Automotive Marketplace
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from app.models import db, NewCar, UsedCar, CarImage, Valuation, RecommendationHistory, User
from app.ml_manager import ml_models
from app.schemas import (
    car_recommendation_schema, car_listing_schema,
    buyback_valuation_schema, price_prediction_schema
)
from app import limiter, csrf
from marshmallow import ValidationError
import json
import os
import uuid
from datetime import datetime
from functools import wraps


def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_image(file, listing_id):
    """Save uploaded image and return the path"""
    if file and allowed_file(file.filename):
        # Create unique filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"car_{listing_id}_{uuid.uuid4().hex[:8]}.{ext}"

        # Ensure upload directory exists
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'static/uploads')
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # Return relative path for database
        return f"uploads/{filename}"
    return None

main_bp = Blueprint('main', __name__)


def optional_jwt(fn):
    """Decorator that allows optional JWT - extracts user if present"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Try to get user from JWT if present
        try:
            from flask_jwt_extended import verify_jwt_in_request
            verify_jwt_in_request(optional=True)
        except Exception:
            pass
        return fn(*args, **kwargs)
    return wrapper


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
@csrf.exempt
@limiter.limit("30 per minute")
@optional_jwt
def get_recommendations():
    """API endpoint to get car recommendations"""
    # Validate input
    try:
        preferences = car_recommendation_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400

    try:
        # Get recommendations from ML model (singleton - loaded once at startup)
        recommendations = ml_models.recommendation_engine.get_recommendations(preferences, top_n=5)

        # Save to history if user is authenticated
        try:
            user_id = get_jwt_identity()
            if user_id:
                history = RecommendationHistory(
                    user_id=user_id,
                    budget_min=preferences['budget_min'],
                    budget_max=preferences['budget_max'],
                    fuel_type=preferences.get('fuel_type'),
                    body_type=preferences.get('body_type'),
                    transmission=preferences.get('transmission'),
                    usage_type=preferences.get('usage_type'),
                    family_size=preferences.get('family_size'),
                    priority_factor=preferences.get('priority_factor'),
                    recommended_cars=json.dumps([r['car_id'] for r in recommendations]),
                    model_used='xgboost_recommendation'
                )
                db.session.add(history)
                db.session.commit()
        except Exception:
            pass  # Don't fail if history save fails

        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'preferences': preferences
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get recommendations. Please try again.'
        }), 500


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


@main_bp.route('/new-car/<int:car_id>')
def new_car_details(car_id):
    """New car details page"""
    car = NewCar.query.filter_by(car_id=car_id).first_or_404()

    # Get similar cars (same brand or body type)
    similar_cars = NewCar.query.filter(
        NewCar.car_id != car_id,
        db.or_(NewCar.brand == car.brand, NewCar.body_type == car.body_type)
    ).order_by(NewCar.safety_rating.desc()).limit(4).all()

    return render_template('recommendations/car_details.html', car=car, similar_cars=similar_cars)


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
@limiter.limit("10 per hour", methods=["POST"])
def list_car():
    """List a car for sale (authentication optional but recommended)"""
    if request.method == 'POST':
        # Check if it's a JSON API request or form submission
        if request.is_json:
            return list_car_api()

        try:
            # Form validation - basic sanitization
            form_data = {
                'brand': request.form.get('brand', '').strip()[:50],
                'model': request.form.get('model', '').strip()[:100],
                'variant': request.form.get('variant', '').strip()[:50],
                'body_type': request.form.get('body_type', '').strip(),
                'registration_year': request.form.get('registration_year'),
                'fuel_type': request.form.get('fuel_type', '').strip(),
                'transmission': request.form.get('transmission', '').strip(),
                'mileage_km': request.form.get('mileage_km'),
                'num_owners': request.form.get('num_owners'),
                'original_price': request.form.get('original_price'),
                'current_price': request.form.get('current_price'),
                'condition_score': request.form.get('condition_score', 70),
                'color': request.form.get('color', '').strip()[:20],
                'city': request.form.get('city', '').strip()[:50],
                'seller_name': request.form.get('seller_name', '').strip()[:100],
                'seller_phone': request.form.get('seller_phone', '').strip()[:20],
            }

            # Basic validation
            required_fields = ['brand', 'model', 'body_type', 'registration_year',
                             'fuel_type', 'transmission', 'current_price', 'seller_name', 'seller_phone']
            for field in required_fields:
                if not form_data.get(field):
                    flash(f'{field.replace("_", " ").title()} is required', 'danger')
                    return render_template('marketplace/list_car.html')

            # Generate unique listing ID using max + 1 pattern (safer than count)
            max_listing = db.session.query(db.func.max(UsedCar.listing_id)).scalar() or 1000
            new_listing_id = max_listing + 1

            registration_year = int(form_data['registration_year'])
            listing = UsedCar(
                listing_id=new_listing_id,
                brand=form_data['brand'],
                model=form_data['model'],
                variant=form_data['variant'] or None,
                body_type=form_data['body_type'],
                registration_year=registration_year,
                age_years=datetime.now().year - registration_year,
                fuel_type=form_data['fuel_type'],
                transmission=form_data['transmission'],
                mileage_km=int(form_data.get('mileage_km') or 0),
                num_owners=int(form_data.get('num_owners') or 1),
                original_price=int(form_data.get('original_price') or form_data['current_price']),
                current_price=int(form_data['current_price']),
                condition_score=float(form_data.get('condition_score') or 70),
                insurance_validity_months=int(request.form.get('insurance_validity_months', 0)),
                service_history=request.form.get('service_history', 'Partial'),
                accident_history=request.form.get('accident_history', 'No'),
                color=form_data['color'] or None,
                seating_capacity=int(request.form.get('seating_capacity', 5)),
                engine_cc=int(request.form.get('engine_cc', 1200)),
                fuel_efficiency_kmpl=float(request.form.get('fuel_efficiency_kmpl', 15)),
                rto=request.form.get('rto', '').strip()[:10] or None,
                city=form_data['city'],
                features=request.form.get('features', '').strip()[:500] or None,
                seller_name=form_data['seller_name'],
                seller_phone=form_data['seller_phone'],
                listing_date=datetime.now().date(),
                negotiable=request.form.get('negotiable', 'No'),
                test_drive_available=request.form.get('test_drive_available', 'Yes'),
                is_sold=False
            )

            db.session.add(listing)
            db.session.flush()  # Get the listing_id before commit

            # Handle uploaded images — save each to CarImage table
            uploaded_files = request.files.getlist('car_images')
            saved_count = 0
            for i, file in enumerate(uploaded_files[:10]):  # max 10 images
                if file and file.filename:
                    image_path = save_uploaded_image(file, listing.listing_id)
                    if image_path:
                        car_image = CarImage(
                            listing_id=listing.listing_id,
                            image_path=image_path,
                            is_primary=(saved_count == 0),
                            display_order=saved_count
                        )
                        db.session.add(car_image)
                        if saved_count == 0:
                            listing.image_path = image_path  # backward compat
                        saved_count += 1

            db.session.commit()

            flash('Your car has been listed successfully!', 'success')
            return redirect(url_for('main.car_details', listing_id=listing.listing_id))

        except ValueError as e:
            db.session.rollback()
            flash('Please enter valid numeric values for price, year, and mileage', 'danger')
        except Exception as e:
            db.session.rollback()
            flash('Error listing car. Please try again.', 'danger')

    return render_template('marketplace/list_car.html')


@main_bp.route('/api/marketplace/list', methods=['POST'])
@csrf.exempt
@jwt_required()
@limiter.limit("10 per hour")
def list_car_api():
    """API endpoint to list a car for sale (requires authentication)"""
    # Validate input
    try:
        data = car_listing_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400

    try:
        user_id = get_jwt_identity()

        # Generate unique listing ID
        max_listing = db.session.query(db.func.max(UsedCar.listing_id)).scalar() or 1000
        new_listing_id = max_listing + 1

        registration_year = data['registration_year']
        listing = UsedCar(
            listing_id=new_listing_id,
            brand=data['brand'],
            model=data['model'],
            variant=data.get('variant'),
            body_type=data['body_type'],
            registration_year=registration_year,
            age_years=datetime.now().year - registration_year,
            fuel_type=data['fuel_type'],
            transmission=data['transmission'],
            mileage_km=data['mileage_km'],
            num_owners=data['num_owners'],
            original_price=data['original_price'],
            current_price=data['current_price'],
            condition_score=data.get('condition_score', 70),
            color=data.get('color'),
            city=data['city'],
            seller_name=data['seller_name'],
            seller_phone=data['seller_phone'],
            listing_date=datetime.now().date(),
            is_sold=False
        )

        db.session.add(listing)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Car listed successfully',
            'listing_id': listing.listing_id,
            'listing': listing.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Failed to list car. Please try again.'
        }), 500


@main_bp.route('/api/predict-price', methods=['POST'])
@csrf.exempt
@limiter.limit("30 per minute")
def predict_price():
    """API endpoint to predict used car price"""
    # Validate input
    try:
        data = price_prediction_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400

    try:
        # Use price predictor (singleton - loaded once at startup)
        predicted_price = ml_models.price_predictor.predict_price(data)

        return jsonify({
            'success': True,
            'predicted_price': int(predicted_price),
            'input_data': data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Price prediction failed. Please try again.'
        }), 500


# ==================== BUY-BACK VALUATION ROUTES ====================

@main_bp.route('/buyback')
def buyback():
    """Buy-back valuation page"""
    return render_template('buyback/form.html')


@main_bp.route('/api/buyback-valuation', methods=['POST'])
@csrf.exempt
@limiter.limit("20 per minute")
@optional_jwt
def buyback_valuation():
    """API endpoint for buy-back valuation"""
    # Validate input
    try:
        data = buyback_valuation_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({
            'success': False,
            'errors': err.messages
        }), 400

    try:
        # Get valuation (singleton - loaded once at startup)
        valuation_result = ml_models.buyback_valuator.get_valuation(data)

        # Get user_id if authenticated
        user_id = None
        try:
            user_id = get_jwt_identity()
        except Exception:
            pass

        # Save valuation to database
        valuation = Valuation(
            user_id=user_id,
            brand=data['brand'],
            model=data['model'],
            variant=data.get('variant'),
            registration_year=data['registration_year'],
            mileage_km=data['mileage_km'],
            num_owners=data['num_owners'],
            fuel_type=data['fuel_type'],
            transmission=data['transmission'],
            service_history=data.get('service_history', 'Partial'),
            accident_history=data.get('accident_history', 'No'),
            insurance_valid=data.get('insurance_valid', False),
            modifications=data.get('modifications', ''),
            condition_score=valuation_result['condition_score'],
            estimated_price_min=valuation_result['estimated_price_min'],
            estimated_price_max=valuation_result['estimated_price_max'],
            estimated_price_avg=valuation_result['estimated_price_avg'],
            confidence_score=valuation_result['confidence_score'],
            customer_name=data['customer_name'],
            customer_phone=data['customer_phone'],
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
            'error': 'Valuation failed. Please try again.'
        }), 500


@main_bp.route('/buyback/valuation/<int:valuation_id>')
def valuation_details(valuation_id):
    """Valuation details page"""
    valuation = Valuation.query.get_or_404(valuation_id)
    return render_template('buyback/valuation_details.html', valuation=valuation)


# ==================== UTILITY ROUTES ====================

@main_bp.route('/health')
@main_bp.route('/api/health')
def health_check():
    """Health check endpoint for monitoring and container orchestration"""
    import time
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'checks': {}
    }

    # Check database connection
    try:
        db.session.execute(db.text('SELECT 1'))
        health_status['checks']['database'] = {'status': 'healthy'}
    except Exception as e:
        health_status['checks']['database'] = {'status': 'unhealthy', 'error': str(e)}
        health_status['status'] = 'unhealthy'

    # Check ML models
    try:
        if ml_models.recommendation_engine and ml_models.price_predictor and ml_models.buyback_valuator:
            health_status['checks']['ml_models'] = {'status': 'healthy'}
        else:
            health_status['checks']['ml_models'] = {'status': 'unhealthy', 'error': 'Models not loaded'}
            health_status['status'] = 'unhealthy'
    except Exception as e:
        health_status['checks']['ml_models'] = {'status': 'unhealthy', 'error': str(e)}
        health_status['status'] = 'unhealthy'

    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code


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
