"""
API Documentation with Swagger/OpenAPI using Flask-RESTX
"""
from flask import Blueprint
from flask_restx import Api, Resource, fields, Namespace

# Create API blueprint
api_bp = Blueprint('api_docs', __name__, url_prefix='/api/docs')

# Initialize API with Swagger documentation
api = Api(
    api_bp,
    version='1.0',
    title='Car Recommendation System API',
    description='API documentation for the Indian Automotive Marketplace',
    doc='/',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Add "Bearer " prefix to your token'
        }
    }
)

# ==================== NAMESPACES ====================

# Authentication namespace
auth_ns = Namespace('auth', description='Authentication operations')

# Cars namespace
cars_ns = Namespace('cars', description='Car operations')

# Recommendations namespace
recommendations_ns = Namespace('recommendations', description='Car recommendation operations')

# Marketplace namespace
marketplace_ns = Namespace('marketplace', description='Used car marketplace operations')

# Buyback namespace
buyback_ns = Namespace('buyback', description='Buy-back valuation operations')

# Register namespaces
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(cars_ns, path='/cars')
api.add_namespace(recommendations_ns, path='/recommendations')
api.add_namespace(marketplace_ns, path='/marketplace')
api.add_namespace(buyback_ns, path='/buyback')

# ==================== MODELS ====================

# User models
user_registration_model = auth_ns.model('UserRegistration', {
    'username': fields.String(required=True, description='Username (3-80 chars)', example='john_doe'),
    'email': fields.String(required=True, description='Email address', example='john@example.com'),
    'password': fields.String(required=True, description='Password (min 8 chars with uppercase, lowercase, digit, special)', example='SecurePass123!'),
    'confirm_password': fields.String(required=True, description='Confirm password'),
    'phone': fields.String(description='Phone number', example='+919876543210'),
    'user_type': fields.String(description='User type', enum=['buyer', 'seller', 'both'], example='buyer')
})

user_login_model = auth_ns.model('UserLogin', {
    'email': fields.String(required=True, description='Email address', example='john@example.com'),
    'password': fields.String(required=True, description='Password', example='SecurePass123!'),
    'remember_me': fields.Boolean(description='Remember me', example=False)
})

token_response_model = auth_ns.model('TokenResponse', {
    'success': fields.Boolean(description='Operation success'),
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'user': fields.Raw(description='User information')
})

# Recommendation models
recommendation_request_model = recommendations_ns.model('RecommendationRequest', {
    'budget_min': fields.Integer(required=True, description='Minimum budget (INR)', example=500000),
    'budget_max': fields.Integer(required=True, description='Maximum budget (INR)', example=1500000),
    'fuel_type': fields.String(description='Preferred fuel type', enum=['Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG', 'any']),
    'body_type': fields.String(description='Preferred body type', enum=['Hatchback', 'Sedan', 'SUV', 'MUV', 'Coupe', 'Convertible', 'any']),
    'transmission': fields.String(description='Preferred transmission', enum=['Manual', 'Automatic', 'any']),
    'usage_type': fields.String(description='Primary usage', enum=['city', 'highway', 'mixed'], example='mixed'),
    'family_size': fields.Integer(description='Family size (1-10)', example=4),
    'priority_factor': fields.String(description='Priority factor', enum=['mileage', 'performance', 'safety', 'comfort', 'overall'])
})

# Buyback models
buyback_request_model = buyback_ns.model('BuybackRequest', {
    'brand': fields.String(required=True, description='Car brand', example='Maruti Suzuki'),
    'model': fields.String(required=True, description='Car model', example='Swift'),
    'body_type': fields.String(required=True, description='Body type', example='Hatchback'),
    'registration_year': fields.Integer(required=True, description='Registration year', example=2019),
    'original_price': fields.Integer(required=True, description='Original purchase price', example=700000),
    'mileage_km': fields.Integer(required=True, description='Odometer reading (km)', example=45000),
    'num_owners': fields.Integer(required=True, description='Number of previous owners', example=1),
    'fuel_type': fields.String(required=True, description='Fuel type', example='Petrol'),
    'transmission': fields.String(required=True, description='Transmission type', example='Manual'),
    'service_history': fields.String(description='Service history', enum=['Complete', 'Partial', 'Unknown']),
    'accident_history': fields.String(description='Accident history', enum=['No', 'Minor', 'Major']),
    'customer_name': fields.String(required=True, description='Customer name', example='John Doe'),
    'customer_phone': fields.String(required=True, description='Customer phone', example='+91-9876543210'),
    'customer_email': fields.String(description='Customer email', example='john@example.com'),
    'inspection_requested': fields.Boolean(description='Request physical inspection', example=False)
})

buyback_response_model = buyback_ns.model('BuybackResponse', {
    'success': fields.Boolean(description='Operation success'),
    'valuation': fields.Raw(description='Valuation details including estimated prices')
})

# Car listing model
car_listing_model = marketplace_ns.model('CarListing', {
    'brand': fields.String(required=True, description='Car brand'),
    'model': fields.String(required=True, description='Car model'),
    'variant': fields.String(description='Car variant'),
    'body_type': fields.String(required=True, description='Body type'),
    'registration_year': fields.Integer(required=True, description='Registration year'),
    'fuel_type': fields.String(required=True, description='Fuel type'),
    'transmission': fields.String(required=True, description='Transmission'),
    'mileage_km': fields.Integer(required=True, description='Mileage in km'),
    'num_owners': fields.Integer(required=True, description='Number of owners'),
    'original_price': fields.Integer(required=True, description='Original price'),
    'current_price': fields.Integer(required=True, description='Asking price'),
    'city': fields.String(required=True, description='City'),
    'seller_name': fields.String(required=True, description='Seller name'),
    'seller_phone': fields.String(required=True, description='Seller phone')
})

# ==================== AUTH ENDPOINTS ====================

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_registration_model)
    @auth_ns.response(201, 'User registered successfully')
    @auth_ns.response(400, 'Validation error')
    @auth_ns.response(409, 'User already exists')
    def post(self):
        """Register a new user"""
        pass  # Actual implementation in auth.py


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_login_model)
    @auth_ns.marshal_with(token_response_model)
    @auth_ns.response(200, 'Login successful')
    @auth_ns.response(401, 'Invalid credentials')
    @auth_ns.response(403, 'Account locked')
    def post(self):
        """Login and get access tokens"""
        pass  # Actual implementation in auth.py


@auth_ns.route('/refresh')
class Refresh(Resource):
    @auth_ns.doc(security='Bearer')
    @auth_ns.response(200, 'Token refreshed')
    @auth_ns.response(401, 'Invalid or expired refresh token')
    def post(self):
        """Refresh access token using refresh token"""
        pass  # Actual implementation in auth.py


# ==================== RECOMMENDATION ENDPOINTS ====================

@recommendations_ns.route('/')
class Recommendations(Resource):
    @recommendations_ns.expect(recommendation_request_model)
    @recommendations_ns.response(200, 'Recommendations retrieved')
    @recommendations_ns.response(400, 'Validation error')
    def post(self):
        """Get car recommendations based on preferences"""
        pass  # Actual implementation in routes.py


# ==================== MARKETPLACE ENDPOINTS ====================

@marketplace_ns.route('/listings')
class Listings(Resource):
    @marketplace_ns.doc(params={
        'page': 'Page number',
        'brand': 'Filter by brand',
        'body_type': 'Filter by body type',
        'price_min': 'Minimum price',
        'price_max': 'Maximum price'
    })
    @marketplace_ns.response(200, 'Listings retrieved')
    def get(self):
        """Get used car listings with optional filters"""
        pass  # Actual implementation in routes.py


@marketplace_ns.route('/list')
class ListCar(Resource):
    @marketplace_ns.expect(car_listing_model)
    @marketplace_ns.doc(security='Bearer')
    @marketplace_ns.response(201, 'Car listed successfully')
    @marketplace_ns.response(400, 'Validation error')
    def post(self):
        """List a car for sale"""
        pass  # Actual implementation in routes.py


# ==================== BUYBACK ENDPOINTS ====================

@buyback_ns.route('/valuation')
class Valuation(Resource):
    @buyback_ns.expect(buyback_request_model)
    @buyback_ns.marshal_with(buyback_response_model)
    @buyback_ns.response(200, 'Valuation completed')
    @buyback_ns.response(400, 'Validation error')
    def post(self):
        """Get instant buy-back valuation for your car"""
        pass  # Actual implementation in routes.py


# ==================== UTILITY ENDPOINTS ====================

@cars_ns.route('/brands')
class Brands(Resource):
    @cars_ns.response(200, 'List of brands')
    def get(self):
        """Get list of all car brands"""
        pass  # Actual implementation in routes.py


@cars_ns.route('/models/<string:brand>')
class Models(Resource):
    @cars_ns.response(200, 'List of models')
    @cars_ns.response(404, 'Brand not found')
    def get(self, brand):
        """Get list of models for a brand"""
        pass  # Actual implementation in routes.py
