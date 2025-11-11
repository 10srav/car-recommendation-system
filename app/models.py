"""
Database models for Indian Automotive Marketplace
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class NewCar(db.Model):
    """Model for new cars inventory"""
    __tablename__ = 'new_cars'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, unique=True, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    variant = db.Column(db.String(50))
    body_type = db.Column(db.String(20))
    year = db.Column(db.Integer)
    price = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(20))
    mileage = db.Column(db.Float)
    transmission = db.Column(db.String(20))
    seating_capacity = db.Column(db.Integer)
    engine_cc = db.Column(db.Integer)
    power_hp = db.Column(db.Integer)
    torque_nm = db.Column(db.Integer)
    safety_rating = db.Column(db.Integer)
    safety_features = db.Column(db.Text)
    comfort_features = db.Column(db.Text)
    ground_clearance_mm = db.Column(db.Integer)
    boot_space_liters = db.Column(db.Integer)
    maintenance_cost_annual = db.Column(db.Integer)
    warranty_years = db.Column(db.Integer)
    colors_available = db.Column(db.Integer)
    resale_value_3yr_percent = db.Column(db.Float)
    resale_value_5yr_percent = db.Column(db.Float)
    city_suitability_score = db.Column(db.Float)
    highway_suitability_score = db.Column(db.Float)
    mileage_score = db.Column(db.Float)
    performance_score = db.Column(db.Float)
    safety_score = db.Column(db.Float)
    comfort_score = db.Column(db.Float)

    def __repr__(self):
        return f'<NewCar {self.brand} {self.model}>'

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'car_id': self.car_id,
            'brand': self.brand,
            'model': self.model,
            'variant': self.variant,
            'body_type': self.body_type,
            'year': self.year,
            'price': self.price,
            'fuel_type': self.fuel_type,
            'mileage': self.mileage,
            'transmission': self.transmission,
            'seating_capacity': self.seating_capacity,
            'engine_cc': self.engine_cc,
            'power_hp': self.power_hp,
            'safety_rating': self.safety_rating,
            'resale_value_3yr_percent': self.resale_value_3yr_percent,
            'resale_value_5yr_percent': self.resale_value_5yr_percent
        }


class UsedCar(db.Model):
    """Model for used cars marketplace"""
    __tablename__ = 'used_cars'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, unique=True, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    variant = db.Column(db.String(50))
    body_type = db.Column(db.String(20))
    registration_year = db.Column(db.Integer)
    age_years = db.Column(db.Integer)
    fuel_type = db.Column(db.String(20))
    transmission = db.Column(db.String(20))
    mileage_km = db.Column(db.Integer)
    num_owners = db.Column(db.Integer)
    original_price = db.Column(db.Integer)
    current_price = db.Column(db.Integer, nullable=False)
    condition_score = db.Column(db.Float)
    insurance_validity_months = db.Column(db.Integer)
    service_history = db.Column(db.String(20))
    accident_history = db.Column(db.String(20))
    color = db.Column(db.String(20))
    seating_capacity = db.Column(db.Integer)
    engine_cc = db.Column(db.Integer)
    fuel_efficiency_kmpl = db.Column(db.Float)
    rto = db.Column(db.String(10))
    city = db.Column(db.String(50))
    features = db.Column(db.Text)
    seller_name = db.Column(db.String(100))
    seller_phone = db.Column(db.String(20))
    listing_date = db.Column(db.Date)
    negotiable = db.Column(db.String(5))
    test_drive_available = db.Column(db.String(5))
    image_path = db.Column(db.String(255))
    is_sold = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<UsedCar {self.brand} {self.model} {self.registration_year}>'

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'listing_id': self.listing_id,
            'brand': self.brand,
            'model': self.model,
            'variant': self.variant,
            'body_type': self.body_type,
            'registration_year': self.registration_year,
            'age_years': self.age_years,
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'mileage_km': self.mileage_km,
            'num_owners': self.num_owners,
            'current_price': self.current_price,
            'condition_score': self.condition_score,
            'city': self.city,
            'features': self.features,
            'seller_phone': self.seller_phone
        }


class User(db.Model):
    """Model for users (buyers/sellers)"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    user_type = db.Column(db.String(20))  # buyer, seller, both
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    recommendations = db.relationship('RecommendationHistory', backref='user', lazy=True)
    valuations = db.relationship('Valuation', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class RecommendationHistory(db.Model):
    """Model for storing recommendation requests"""
    __tablename__ = 'recommendation_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    budget_min = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    fuel_type = db.Column(db.String(20))
    body_type = db.Column(db.String(20))
    transmission = db.Column(db.String(20))
    usage_type = db.Column(db.String(20))  # city, highway, mixed
    family_size = db.Column(db.Integer)
    priority_factor = db.Column(db.String(50))  # mileage, performance, safety, comfort
    recommended_cars = db.Column(db.Text)  # JSON string of car IDs
    model_used = db.Column(db.String(50))  # Which ML model was used
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Recommendation {self.id}>'


class Valuation(db.Model):
    """Model for buy-back valuation requests"""
    __tablename__ = 'valuations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    variant = db.Column(db.String(50))
    registration_year = db.Column(db.Integer, nullable=False)
    mileage_km = db.Column(db.Integer, nullable=False)
    num_owners = db.Column(db.Integer, nullable=False)
    fuel_type = db.Column(db.String(20))
    transmission = db.Column(db.String(20))
    service_history = db.Column(db.String(20))
    accident_history = db.Column(db.String(20))
    insurance_valid = db.Column(db.Boolean)
    modifications = db.Column(db.Text)
    condition_score = db.Column(db.Float)

    # Valuation results
    estimated_price_min = db.Column(db.Integer)
    estimated_price_max = db.Column(db.Integer)
    estimated_price_avg = db.Column(db.Integer)
    confidence_score = db.Column(db.Float)

    # Contact and status
    customer_name = db.Column(db.String(100))
    customer_phone = db.Column(db.String(20))
    customer_email = db.Column(db.String(120))
    inspection_requested = db.Column(db.Boolean, default=False)
    inspection_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')  # pending, inspected, offered, completed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Valuation {self.brand} {self.model} {self.registration_year}>'

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'variant': self.variant,
            'registration_year': self.registration_year,
            'mileage_km': self.mileage_km,
            'num_owners': self.num_owners,
            'estimated_price_min': self.estimated_price_min,
            'estimated_price_max': self.estimated_price_max,
            'estimated_price_avg': self.estimated_price_avg,
            'confidence_score': self.confidence_score,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class Transaction(db.Model):
    """Model for tracking transactions"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer)  # Reference to used car listing
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    transaction_type = db.Column(db.String(20))  # used_car_sale, buy_back
    amount = db.Column(db.Integer)
    status = db.Column(db.String(20))  # initiated, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Transaction {self.id}>'
