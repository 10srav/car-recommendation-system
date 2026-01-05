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
    brand = db.Column(db.String(50), nullable=False, index=True)
    model = db.Column(db.String(100), nullable=False)
    variant = db.Column(db.String(50))
    body_type = db.Column(db.String(20), index=True)
    year = db.Column(db.Integer)
    price = db.Column(db.Integer, nullable=False, index=True)
    fuel_type = db.Column(db.String(20), index=True)
    mileage = db.Column(db.Float)
    transmission = db.Column(db.String(20), index=True)
    seating_capacity = db.Column(db.Integer)
    engine_cc = db.Column(db.Integer)
    power_hp = db.Column(db.Integer)
    torque_nm = db.Column(db.Integer)
    safety_rating = db.Column(db.Integer, index=True)
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
    brand = db.Column(db.String(50), nullable=False, index=True)
    model = db.Column(db.String(100), nullable=False)
    variant = db.Column(db.String(50))
    body_type = db.Column(db.String(20), index=True)
    registration_year = db.Column(db.Integer, index=True)
    age_years = db.Column(db.Integer)
    fuel_type = db.Column(db.String(20), index=True)
    transmission = db.Column(db.String(20), index=True)
    mileage_km = db.Column(db.Integer)
    num_owners = db.Column(db.Integer)
    original_price = db.Column(db.Integer)
    current_price = db.Column(db.Integer, nullable=False, index=True)
    condition_score = db.Column(db.Float, index=True)
    insurance_validity_months = db.Column(db.Integer)
    service_history = db.Column(db.String(20))
    accident_history = db.Column(db.String(20))
    color = db.Column(db.String(20))
    seating_capacity = db.Column(db.Integer)
    engine_cc = db.Column(db.Integer)
    fuel_efficiency_kmpl = db.Column(db.Float)
    rto = db.Column(db.String(10))
    city = db.Column(db.String(50), index=True)
    features = db.Column(db.Text)
    seller_name = db.Column(db.String(100))
    seller_phone = db.Column(db.String(20))
    listing_date = db.Column(db.Date, index=True)
    negotiable = db.Column(db.String(5))
    test_drive_available = db.Column(db.String(5))
    image_path = db.Column(db.String(255))
    is_sold = db.Column(db.Boolean, default=False, index=True)

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
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    user_type = db.Column(db.String(20), default='buyer')  # buyer, seller, both
    role = db.Column(db.String(20), default='user', index=True)  # user, admin, moderator

    # Account status
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_verified = db.Column(db.Boolean, default=False)
    verified_at = db.Column(db.DateTime)

    # Security fields
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))  # Supports IPv6

    # Profile
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    recommendations = db.relationship('RecommendationHistory', backref='user', lazy=True)
    valuations = db.relationship('Valuation', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash and set the password"""
        from flask_bcrypt import generate_password_hash
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches the hash"""
        from flask_bcrypt import check_password_hash
        return check_password_hash(self.password_hash, password)

    def is_locked(self):
        """Check if the account is locked"""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until

    def increment_failed_login(self):
        """Increment failed login attempts and lock if necessary"""
        self.failed_login_attempts += 1
        # Lock account after 5 failed attempts for 30 minutes
        if self.failed_login_attempts >= 5:
            from datetime import timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)

    def reset_failed_login(self):
        """Reset failed login attempts on successful login"""
        self.failed_login_attempts = 0
        self.locked_until = None

    def to_dict(self, include_private=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email if include_private else None,
            'user_type': self.user_type,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_private:
            data['phone'] = self.phone
            data['role'] = self.role
            data['is_active'] = self.is_active
            data['last_login'] = self.last_login.isoformat() if self.last_login else None
        return data


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
    customer_email = db.Column(db.String(120), index=True)
    inspection_requested = db.Column(db.Boolean, default=False)
    inspection_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending', index=True)  # pending, inspected, offered, completed

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

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
