"""
Marshmallow schemas for input validation and serialization
"""
from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
import re


class UserRegistrationSchema(Schema):
    """Schema for user registration validation"""
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=80, error="Username must be 3-80 characters"),
            validate.Regexp(
                r'^[a-zA-Z0-9_]+$',
                error="Username can only contain letters, numbers, and underscores"
            )
        ]
    )
    email = fields.Email(required=True, error_messages={"invalid": "Invalid email address"})
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128, error="Password must be 8-128 characters")
    )
    confirm_password = fields.Str(required=True, load_only=True)
    phone = fields.Str(
        validate=validate.Regexp(
            r'^\+?[1-9]\d{9,14}$',
            error="Invalid phone number format"
        ),
        allow_none=True
    )
    user_type = fields.Str(
        validate=validate.OneOf(['buyer', 'seller', 'both']),
        load_default='buyer'
    )
    first_name = fields.Str(validate=validate.Length(max=50), allow_none=True)
    last_name = fields.Str(validate=validate.Length(max=50), allow_none=True)

    @validates('password')
    def validate_password_strength(self, value, **kwargs):
        """Validate password meets security requirements"""
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', value):
            raise ValidationError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("Password must contain at least one special character")

    @post_load
    def check_passwords_match(self, data, **kwargs):
        """Verify password and confirm_password match"""
        if data.get('password') != data.get('confirm_password'):
            raise ValidationError("Passwords do not match", field_name='confirm_password')
        # Remove confirm_password from data
        data.pop('confirm_password', None)
        return data


class UserLoginSchema(Schema):
    """Schema for user login validation"""
    email = fields.Email(required=True, error_messages={"invalid": "Invalid email address"})
    password = fields.Str(required=True, load_only=True)
    remember_me = fields.Bool(load_default=False)


class UserUpdateSchema(Schema):
    """Schema for updating user profile"""
    username = fields.Str(
        validate=[
            validate.Length(min=3, max=80),
            validate.Regexp(r'^[a-zA-Z0-9_]+$')
        ]
    )
    phone = fields.Str(
        validate=validate.Regexp(r'^\+?[1-9]\d{9,14}$'),
        allow_none=True
    )
    user_type = fields.Str(validate=validate.OneOf(['buyer', 'seller', 'both']))
    first_name = fields.Str(validate=validate.Length(max=50), allow_none=True)
    last_name = fields.Str(validate=validate.Length(max=50), allow_none=True)


class PasswordChangeSchema(Schema):
    """Schema for password change"""
    current_password = fields.Str(required=True, load_only=True)
    new_password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128)
    )
    confirm_new_password = fields.Str(required=True, load_only=True)

    @validates('new_password')
    def validate_password_strength(self, value, **kwargs):
        """Validate password meets security requirements"""
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', value):
            raise ValidationError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("Password must contain at least one special character")

    @post_load
    def check_passwords_match(self, data, **kwargs):
        """Verify new passwords match"""
        if data.get('new_password') != data.get('confirm_new_password'):
            raise ValidationError("New passwords do not match", field_name='confirm_new_password')
        data.pop('confirm_new_password', None)
        return data


class CarRecommendationSchema(Schema):
    """Schema for car recommendation requests"""
    budget_min = fields.Int(
        required=True,
        validate=validate.Range(min=100000, max=100000000, error="Budget must be between 1 lakh and 10 crore")
    )
    budget_max = fields.Int(
        required=True,
        validate=validate.Range(min=100000, max=100000000)
    )
    fuel_type = fields.Str(
        validate=validate.OneOf(['Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG', 'any']),
        allow_none=True
    )
    body_type = fields.Str(
        validate=validate.OneOf(['Hatchback', 'Sedan', 'SUV', 'MUV', 'Coupe', 'Convertible', 'any']),
        allow_none=True
    )
    transmission = fields.Str(
        validate=validate.OneOf(['Manual', 'Automatic', 'any']),
        allow_none=True
    )
    usage_type = fields.Str(
        validate=validate.OneOf(['city', 'highway', 'mixed']),
        load_default='mixed'
    )
    family_size = fields.Int(
        validate=validate.Range(min=1, max=10),
        load_default=4
    )
    priority_factor = fields.Str(
        validate=validate.OneOf(['mileage', 'performance', 'safety', 'comfort', 'overall']),
        load_default='overall'
    )

    @post_load
    def validate_budget_range(self, data, **kwargs):
        """Ensure budget_min is less than budget_max"""
        if data['budget_min'] > data['budget_max']:
            raise ValidationError("Minimum budget cannot be greater than maximum budget")
        return data


class CarListingSchema(Schema):
    """Schema for listing a car for sale"""
    brand = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    model = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    variant = fields.Str(validate=validate.Length(max=50), allow_none=True)
    body_type = fields.Str(
        required=True,
        validate=validate.OneOf(['Hatchback', 'Sedan', 'SUV', 'MUV', 'Coupe', 'Convertible'])
    )
    registration_year = fields.Int(
        required=True,
        validate=validate.Range(min=1990, max=2026)
    )
    fuel_type = fields.Str(
        required=True,
        validate=validate.OneOf(['Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG'])
    )
    transmission = fields.Str(
        required=True,
        validate=validate.OneOf(['Manual', 'Automatic'])
    )
    mileage_km = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=1000000)
    )
    num_owners = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=10)
    )
    original_price = fields.Int(
        required=True,
        validate=validate.Range(min=50000, max=100000000)
    )
    current_price = fields.Int(
        required=True,
        validate=validate.Range(min=25000, max=100000000)
    )
    condition_score = fields.Float(
        validate=validate.Range(min=0, max=100),
        load_default=70.0
    )
    color = fields.Str(validate=validate.Length(max=20), allow_none=True)
    city = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    seller_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    seller_phone = fields.Str(
        required=True,
        validate=validate.Regexp(r'^\+?[1-9]\d{9,14}$', error="Invalid phone number")
    )


class BuybackValuationSchema(Schema):
    """Schema for buy-back valuation requests"""
    brand = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    model = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    variant = fields.Str(validate=validate.Length(max=50), allow_none=True)
    registration_year = fields.Int(
        required=True,
        validate=validate.Range(min=1990, max=2026)
    )
    mileage_km = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=1000000)
    )
    num_owners = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=10)
    )
    fuel_type = fields.Str(
        required=True,
        validate=validate.OneOf(['Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG'])
    )
    transmission = fields.Str(
        required=True,
        validate=validate.OneOf(['Manual', 'Automatic'])
    )
    service_history = fields.Str(
        validate=validate.OneOf(['Full', 'Partial', 'None']),
        load_default='Partial'
    )
    accident_history = fields.Str(
        validate=validate.OneOf(['Yes', 'No', 'Minor']),
        load_default='No'
    )
    insurance_valid = fields.Bool(load_default=False)
    modifications = fields.Str(validate=validate.Length(max=500), allow_none=True)
    customer_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    customer_phone = fields.Str(
        required=True,
        validate=validate.Regexp(r'^\+?[1-9]\d{9,14}$', error="Invalid phone number")
    )
    customer_email = fields.Email(required=True)
    inspection_requested = fields.Bool(load_default=False)


class PricePredictionSchema(Schema):
    """Schema for price prediction requests"""
    brand = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    body_type = fields.Str(
        required=True,
        validate=validate.OneOf(['Hatchback', 'Sedan', 'SUV', 'MUV', 'Coupe', 'Convertible'])
    )
    registration_year = fields.Int(
        required=True,
        validate=validate.Range(min=1990, max=2026)
    )
    fuel_type = fields.Str(
        required=True,
        validate=validate.OneOf(['Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG'])
    )
    transmission = fields.Str(
        required=True,
        validate=validate.OneOf(['Manual', 'Automatic'])
    )
    mileage_km = fields.Int(
        required=True,
        validate=validate.Range(min=0, max=1000000)
    )
    num_owners = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=10)
    )
    original_price = fields.Int(
        required=True,
        validate=validate.Range(min=50000, max=100000000)
    )
    condition_score = fields.Float(
        validate=validate.Range(min=0, max=100),
        load_default=70.0
    )
    service_history = fields.Str(
        validate=validate.OneOf(['Full', 'Partial', 'None']),
        load_default='Partial'
    )
    accident_history = fields.Str(
        validate=validate.OneOf(['Yes', 'No', 'Minor']),
        load_default='No'
    )


# Schema instances for easy import
user_registration_schema = UserRegistrationSchema()
user_login_schema = UserLoginSchema()
user_update_schema = UserUpdateSchema()
password_change_schema = PasswordChangeSchema()
car_recommendation_schema = CarRecommendationSchema()
car_listing_schema = CarListingSchema()
buyback_valuation_schema = BuybackValuationSchema()
price_prediction_schema = PricePredictionSchema()
