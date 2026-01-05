"""
Unit tests for Marshmallow schemas
"""
import pytest
from marshmallow import ValidationError
from app.schemas import (
    user_registration_schema, user_login_schema,
    user_update_schema, password_change_schema,
    car_recommendation_schema, car_listing_schema,
    buyback_valuation_schema, price_prediction_schema
)


class TestUserRegistrationSchema:
    """Tests for UserRegistrationSchema"""

    def test_valid_registration(self):
        """Test valid registration data passes validation"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'phone': '+919876543210',
            'user_type': 'buyer',
            'first_name': 'Test',
            'last_name': 'User'
        }
        result = user_registration_schema.load(data)
        assert result['username'] == 'testuser'
        assert result['email'] == 'test@example.com'
        assert 'confirm_password' not in result  # Should be removed

    def test_missing_required_username(self):
        """Test missing username fails"""
        data = {
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'username' in exc.value.messages

    def test_missing_required_email(self):
        """Test missing email fails"""
        data = {
            'username': 'testuser',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'email' in exc.value.messages

    def test_invalid_email_format(self):
        """Test invalid email format fails"""
        data = {
            'username': 'testuser',
            'email': 'not-an-email',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'email' in exc.value.messages

    def test_username_too_short(self):
        """Test username less than 3 characters fails"""
        data = {
            'username': 'ab',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'username' in exc.value.messages

    def test_username_invalid_characters(self):
        """Test username with special characters fails"""
        data = {
            'username': 'test@user!',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'username' in exc.value.messages

    def test_password_no_uppercase(self):
        """Test password without uppercase fails"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepass123!',
            'confirm_password': 'securepass123!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'password' in exc.value.messages
        assert 'uppercase' in str(exc.value.messages['password'][0]).lower()

    def test_password_no_lowercase(self):
        """Test password without lowercase fails"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SECUREPASS123!',
            'confirm_password': 'SECUREPASS123!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'password' in exc.value.messages
        assert 'lowercase' in str(exc.value.messages['password'][0]).lower()

    def test_password_no_digit(self):
        """Test password without digit fails"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass!!!',
            'confirm_password': 'SecurePass!!!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'password' in exc.value.messages
        assert 'digit' in str(exc.value.messages['password'][0]).lower()

    def test_password_no_special_char(self):
        """Test password without special character fails"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123',
            'confirm_password': 'SecurePass123'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'password' in exc.value.messages
        assert 'special' in str(exc.value.messages['password'][0]).lower()

    def test_password_too_short(self):
        """Test password less than 8 characters fails"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Pass1!',
            'confirm_password': 'Pass1!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'password' in exc.value.messages

    def test_password_mismatch(self):
        """Test mismatched passwords fail"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'DifferentPass123!'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'confirm_password' in exc.value.messages

    def test_invalid_phone_format(self):
        """Test invalid phone number fails"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'phone': '123'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'phone' in exc.value.messages

    def test_invalid_user_type(self):
        """Test invalid user_type fails"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'user_type': 'invalid'
        }
        with pytest.raises(ValidationError) as exc:
            user_registration_schema.load(data)
        assert 'user_type' in exc.value.messages

    def test_default_user_type(self):
        """Test default user_type is buyer"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        }
        result = user_registration_schema.load(data)
        assert result['user_type'] == 'buyer'

    def test_optional_fields_can_be_none(self):
        """Test optional fields can be None"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'phone': None,
            'first_name': None,
            'last_name': None
        }
        result = user_registration_schema.load(data)
        assert result['phone'] is None


class TestUserLoginSchema:
    """Tests for UserLoginSchema"""

    def test_valid_login(self):
        """Test valid login data"""
        data = {
            'email': 'test@example.com',
            'password': 'anypassword'
        }
        result = user_login_schema.load(data)
        assert result['email'] == 'test@example.com'
        assert result['remember_me'] is False  # Default

    def test_login_with_remember_me(self):
        """Test login with remember_me flag"""
        data = {
            'email': 'test@example.com',
            'password': 'anypassword',
            'remember_me': True
        }
        result = user_login_schema.load(data)
        assert result['remember_me'] is True

    def test_missing_email(self):
        """Test missing email fails"""
        data = {'password': 'anypassword'}
        with pytest.raises(ValidationError) as exc:
            user_login_schema.load(data)
        assert 'email' in exc.value.messages

    def test_missing_password(self):
        """Test missing password fails"""
        data = {'email': 'test@example.com'}
        with pytest.raises(ValidationError) as exc:
            user_login_schema.load(data)
        assert 'password' in exc.value.messages

    def test_invalid_email(self):
        """Test invalid email fails"""
        data = {
            'email': 'invalid-email',
            'password': 'anypassword'
        }
        with pytest.raises(ValidationError) as exc:
            user_login_schema.load(data)
        assert 'email' in exc.value.messages


class TestUserUpdateSchema:
    """Tests for UserUpdateSchema"""

    def test_valid_update(self):
        """Test valid update data"""
        data = {
            'username': 'newusername',
            'phone': '+919876543210',
            'user_type': 'seller',
            'first_name': 'New',
            'last_name': 'Name'
        }
        result = user_update_schema.load(data)
        assert result['username'] == 'newusername'

    def test_partial_update(self):
        """Test partial update with some fields"""
        data = {'first_name': 'Updated'}
        result = user_update_schema.load(data)
        assert result['first_name'] == 'Updated'
        assert 'username' not in result

    def test_empty_update(self):
        """Test empty update data is valid"""
        data = {}
        result = user_update_schema.load(data)
        assert result == {}

    def test_invalid_username(self):
        """Test invalid username fails"""
        data = {'username': 'ab'}  # Too short
        with pytest.raises(ValidationError) as exc:
            user_update_schema.load(data)
        assert 'username' in exc.value.messages


class TestPasswordChangeSchema:
    """Tests for PasswordChangeSchema"""

    def test_valid_password_change(self):
        """Test valid password change data"""
        data = {
            'current_password': 'OldPass123!',
            'new_password': 'NewSecure456@',
            'confirm_new_password': 'NewSecure456@'
        }
        result = password_change_schema.load(data)
        assert result['current_password'] == 'OldPass123!'
        assert result['new_password'] == 'NewSecure456@'
        assert 'confirm_new_password' not in result

    def test_new_password_no_uppercase(self):
        """Test new password without uppercase fails"""
        data = {
            'current_password': 'OldPass123!',
            'new_password': 'newsecure456@',
            'confirm_new_password': 'newsecure456@'
        }
        with pytest.raises(ValidationError) as exc:
            password_change_schema.load(data)
        assert 'new_password' in exc.value.messages

    def test_new_password_mismatch(self):
        """Test mismatched new passwords fail"""
        data = {
            'current_password': 'OldPass123!',
            'new_password': 'NewSecure456@',
            'confirm_new_password': 'DifferentPass789#'
        }
        with pytest.raises(ValidationError) as exc:
            password_change_schema.load(data)
        assert 'confirm_new_password' in exc.value.messages

    def test_missing_current_password(self):
        """Test missing current password fails"""
        data = {
            'new_password': 'NewSecure456@',
            'confirm_new_password': 'NewSecure456@'
        }
        with pytest.raises(ValidationError) as exc:
            password_change_schema.load(data)
        assert 'current_password' in exc.value.messages

    def test_new_password_no_lowercase(self):
        """Test new password without lowercase fails"""
        data = {
            'current_password': 'OldPass123!',
            'new_password': 'NEWSECURE456@',
            'confirm_new_password': 'NEWSECURE456@'
        }
        with pytest.raises(ValidationError) as exc:
            password_change_schema.load(data)
        assert 'new_password' in exc.value.messages
        assert 'lowercase' in str(exc.value.messages['new_password'][0]).lower()

    def test_new_password_no_digit(self):
        """Test new password without digit fails"""
        data = {
            'current_password': 'OldPass123!',
            'new_password': 'NewSecurePass@',
            'confirm_new_password': 'NewSecurePass@'
        }
        with pytest.raises(ValidationError) as exc:
            password_change_schema.load(data)
        assert 'new_password' in exc.value.messages
        assert 'digit' in str(exc.value.messages['new_password'][0]).lower()

    def test_new_password_no_special_char(self):
        """Test new password without special character fails"""
        data = {
            'current_password': 'OldPass123!',
            'new_password': 'NewSecure456',
            'confirm_new_password': 'NewSecure456'
        }
        with pytest.raises(ValidationError) as exc:
            password_change_schema.load(data)
        assert 'new_password' in exc.value.messages
        assert 'special' in str(exc.value.messages['new_password'][0]).lower()


class TestCarRecommendationSchema:
    """Tests for CarRecommendationSchema"""

    def test_valid_recommendation_request(self):
        """Test valid recommendation request"""
        data = {
            'budget_min': 500000,
            'budget_max': 1500000,
            'fuel_type': 'Petrol',
            'body_type': 'SUV',
            'transmission': 'Automatic'
        }
        result = car_recommendation_schema.load(data)
        assert result['budget_min'] == 500000
        assert result['usage_type'] == 'mixed'  # Default
        assert result['family_size'] == 4  # Default
        assert result['priority_factor'] == 'overall'  # Default

    def test_budget_min_too_low(self):
        """Test budget below minimum fails"""
        data = {
            'budget_min': 50000,  # Below 100000
            'budget_max': 1000000
        }
        with pytest.raises(ValidationError) as exc:
            car_recommendation_schema.load(data)
        assert 'budget_min' in exc.value.messages

    def test_budget_max_too_high(self):
        """Test budget above maximum fails"""
        data = {
            'budget_min': 500000,
            'budget_max': 200000000  # Above 100000000
        }
        with pytest.raises(ValidationError) as exc:
            car_recommendation_schema.load(data)
        assert 'budget_max' in exc.value.messages

    def test_budget_min_greater_than_max(self):
        """Test budget_min > budget_max fails"""
        data = {
            'budget_min': 2000000,
            'budget_max': 1000000
        }
        with pytest.raises(ValidationError) as exc:
            car_recommendation_schema.load(data)
        assert 'Minimum budget cannot be greater' in str(exc.value.messages)

    def test_invalid_fuel_type(self):
        """Test invalid fuel type fails"""
        data = {
            'budget_min': 500000,
            'budget_max': 1000000,
            'fuel_type': 'Nuclear'
        }
        with pytest.raises(ValidationError) as exc:
            car_recommendation_schema.load(data)
        assert 'fuel_type' in exc.value.messages

    def test_invalid_body_type(self):
        """Test invalid body type fails"""
        data = {
            'budget_min': 500000,
            'budget_max': 1000000,
            'body_type': 'Spaceship'
        }
        with pytest.raises(ValidationError) as exc:
            car_recommendation_schema.load(data)
        assert 'body_type' in exc.value.messages

    def test_family_size_out_of_range(self):
        """Test family size out of range fails"""
        data = {
            'budget_min': 500000,
            'budget_max': 1000000,
            'family_size': 15
        }
        with pytest.raises(ValidationError) as exc:
            car_recommendation_schema.load(data)
        assert 'family_size' in exc.value.messages

    def test_all_optional_filters(self):
        """Test all optional filter values"""
        data = {
            'budget_min': 500000,
            'budget_max': 1500000,
            'fuel_type': 'any',
            'body_type': 'any',
            'transmission': 'any',
            'usage_type': 'highway',
            'family_size': 6,
            'priority_factor': 'safety'
        }
        result = car_recommendation_schema.load(data)
        assert result['priority_factor'] == 'safety'


class TestCarListingSchema:
    """Tests for CarListingSchema"""

    def test_valid_car_listing(self):
        """Test valid car listing data"""
        data = {
            'brand': 'Honda',
            'model': 'City',
            'variant': 'V CVT',
            'body_type': 'Sedan',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 1200000,
            'current_price': 800000,
            'condition_score': 85.0,
            'color': 'White',
            'city': 'Mumbai',
            'seller_name': 'John Doe',
            'seller_phone': '+919876543210'
        }
        result = car_listing_schema.load(data)
        assert result['brand'] == 'Honda'
        assert result['condition_score'] == 85.0

    def test_missing_required_brand(self):
        """Test missing brand fails"""
        data = {
            'model': 'City',
            'body_type': 'Sedan',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 1200000,
            'current_price': 800000,
            'city': 'Mumbai',
            'seller_name': 'John',
            'seller_phone': '+919876543210'
        }
        with pytest.raises(ValidationError) as exc:
            car_listing_schema.load(data)
        assert 'brand' in exc.value.messages

    def test_invalid_registration_year(self):
        """Test registration year out of range fails"""
        data = {
            'brand': 'Honda',
            'model': 'City',
            'body_type': 'Sedan',
            'registration_year': 1980,  # Before 1990
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 1200000,
            'current_price': 800000,
            'city': 'Mumbai',
            'seller_name': 'John',
            'seller_phone': '+919876543210'
        }
        with pytest.raises(ValidationError) as exc:
            car_listing_schema.load(data)
        assert 'registration_year' in exc.value.messages

    def test_invalid_seller_phone(self):
        """Test invalid seller phone fails"""
        data = {
            'brand': 'Honda',
            'model': 'City',
            'body_type': 'Sedan',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 1200000,
            'current_price': 800000,
            'city': 'Mumbai',
            'seller_name': 'John',
            'seller_phone': '123'  # Invalid
        }
        with pytest.raises(ValidationError) as exc:
            car_listing_schema.load(data)
        assert 'seller_phone' in exc.value.messages

    def test_default_condition_score(self):
        """Test default condition score is 70"""
        data = {
            'brand': 'Honda',
            'model': 'City',
            'body_type': 'Sedan',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 1200000,
            'current_price': 800000,
            'city': 'Mumbai',
            'seller_name': 'John Doe',
            'seller_phone': '+919876543210'
        }
        result = car_listing_schema.load(data)
        assert result['condition_score'] == 70.0

    def test_mileage_out_of_range(self):
        """Test mileage above maximum fails"""
        data = {
            'brand': 'Honda',
            'model': 'City',
            'body_type': 'Sedan',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'mileage_km': 2000000,  # Above 1000000
            'num_owners': 1,
            'original_price': 1200000,
            'current_price': 800000,
            'city': 'Mumbai',
            'seller_name': 'John',
            'seller_phone': '+919876543210'
        }
        with pytest.raises(ValidationError) as exc:
            car_listing_schema.load(data)
        assert 'mileage_km' in exc.value.messages


class TestBuybackValuationSchema:
    """Tests for BuybackValuationSchema"""

    def test_valid_buyback_request(self):
        """Test valid buyback valuation request"""
        data = {
            'brand': 'Maruti Suzuki',
            'model': 'Swift',
            'registration_year': 2019,
            'mileage_km': 45000,
            'num_owners': 1,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'customer_name': 'John Doe',
            'customer_phone': '+919876543210',
            'customer_email': 'john@example.com'
        }
        result = buyback_valuation_schema.load(data)
        assert result['brand'] == 'Maruti Suzuki'
        assert result['service_history'] == 'Partial'  # Default
        assert result['accident_history'] == 'No'  # Default
        assert result['insurance_valid'] is False  # Default
        assert result['inspection_requested'] is False  # Default

    def test_with_optional_fields(self):
        """Test buyback with all optional fields"""
        data = {
            'brand': 'Honda',
            'model': 'City',
            'variant': 'V CVT',
            'registration_year': 2020,
            'mileage_km': 30000,
            'num_owners': 1,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'service_history': 'Full',
            'accident_history': 'Minor',
            'insurance_valid': True,
            'modifications': 'Alloy wheels, tinted windows',
            'customer_name': 'Jane Doe',
            'customer_phone': '+919876543211',
            'customer_email': 'jane@example.com',
            'inspection_requested': True
        }
        result = buyback_valuation_schema.load(data)
        assert result['service_history'] == 'Full'
        assert result['inspection_requested'] is True

    def test_invalid_customer_email(self):
        """Test invalid customer email fails"""
        data = {
            'brand': 'Maruti',
            'model': 'Swift',
            'registration_year': 2019,
            'mileage_km': 45000,
            'num_owners': 1,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'customer_name': 'John',
            'customer_phone': '+919876543210',
            'customer_email': 'not-an-email'
        }
        with pytest.raises(ValidationError) as exc:
            buyback_valuation_schema.load(data)
        assert 'customer_email' in exc.value.messages

    def test_invalid_service_history(self):
        """Test invalid service history fails"""
        data = {
            'brand': 'Maruti',
            'model': 'Swift',
            'registration_year': 2019,
            'mileage_km': 45000,
            'num_owners': 1,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'service_history': 'Unknown',
            'customer_name': 'John',
            'customer_phone': '+919876543210',
            'customer_email': 'john@example.com'
        }
        with pytest.raises(ValidationError) as exc:
            buyback_valuation_schema.load(data)
        assert 'service_history' in exc.value.messages

    def test_modifications_too_long(self):
        """Test modifications exceeding max length fails"""
        data = {
            'brand': 'Maruti',
            'model': 'Swift',
            'registration_year': 2019,
            'mileage_km': 45000,
            'num_owners': 1,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'modifications': 'x' * 501,  # Exceeds 500
            'customer_name': 'John',
            'customer_phone': '+919876543210',
            'customer_email': 'john@example.com'
        }
        with pytest.raises(ValidationError) as exc:
            buyback_valuation_schema.load(data)
        assert 'modifications' in exc.value.messages


class TestPricePredictionSchema:
    """Tests for PricePredictionSchema"""

    def test_valid_price_prediction(self):
        """Test valid price prediction request"""
        data = {
            'brand': 'Maruti Suzuki',
            'body_type': 'Hatchback',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 800000
        }
        result = price_prediction_schema.load(data)
        assert result['brand'] == 'Maruti Suzuki'
        assert result['condition_score'] == 70.0  # Default
        assert result['service_history'] == 'Partial'  # Default
        assert result['accident_history'] == 'No'  # Default

    def test_with_all_fields(self):
        """Test price prediction with all optional fields"""
        data = {
            'brand': 'Honda',
            'body_type': 'Sedan',
            'registration_year': 2019,
            'fuel_type': 'Diesel',
            'transmission': 'Automatic',
            'mileage_km': 50000,
            'num_owners': 2,
            'original_price': 1500000,
            'condition_score': 80.0,
            'service_history': 'Full',
            'accident_history': 'Minor'
        }
        result = price_prediction_schema.load(data)
        assert result['condition_score'] == 80.0
        assert result['accident_history'] == 'Minor'

    def test_missing_required_field(self):
        """Test missing required field fails"""
        data = {
            'brand': 'Maruti',
            # Missing body_type
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 800000
        }
        with pytest.raises(ValidationError) as exc:
            price_prediction_schema.load(data)
        assert 'body_type' in exc.value.messages

    def test_invalid_original_price(self):
        """Test original price below minimum fails"""
        data = {
            'brand': 'Maruti',
            'body_type': 'Hatchback',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 10000  # Below 50000
        }
        with pytest.raises(ValidationError) as exc:
            price_prediction_schema.load(data)
        assert 'original_price' in exc.value.messages

    def test_condition_score_out_of_range(self):
        """Test condition score above 100 fails"""
        data = {
            'brand': 'Maruti',
            'body_type': 'Hatchback',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 800000,
            'condition_score': 150  # Above 100
        }
        with pytest.raises(ValidationError) as exc:
            price_prediction_schema.load(data)
        assert 'condition_score' in exc.value.messages

    def test_all_body_types(self):
        """Test all valid body types"""
        base_data = {
            'brand': 'Test',
            'registration_year': 2020,
            'fuel_type': 'Petrol',
            'transmission': 'Manual',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 800000
        }

        valid_types = ['Hatchback', 'Sedan', 'SUV', 'MUV', 'Coupe', 'Convertible']
        for body_type in valid_types:
            data = {**base_data, 'body_type': body_type}
            result = price_prediction_schema.load(data)
            assert result['body_type'] == body_type

    def test_all_fuel_types(self):
        """Test all valid fuel types"""
        base_data = {
            'brand': 'Test',
            'body_type': 'Sedan',
            'registration_year': 2020,
            'transmission': 'Manual',
            'mileage_km': 30000,
            'num_owners': 1,
            'original_price': 800000
        }

        valid_types = ['Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG']
        for fuel_type in valid_types:
            data = {**base_data, 'fuel_type': fuel_type}
            result = price_prediction_schema.load(data)
            assert result['fuel_type'] == fuel_type
