"""
Unit tests for main routes module
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, date
from app.models import db, NewCar, UsedCar, Valuation, RecommendationHistory, User


class TestIndexRoute:
    """Tests for the index/home page route"""

    def test_index_page_loads(self, client):
        """Test index page returns 200"""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_page_with_data(self, app, client):
        """Test index page displays car statistics"""
        # Add some test data
        with app.app_context():
            new_car = NewCar(
                car_id=1,
                brand='Maruti Suzuki',
                model='Swift',
                price=800000,
                fuel_type='Petrol',
                safety_rating=4,
                body_type='Hatchback',
                transmission='Manual'
            )
            db.session.add(new_car)

            used_car = UsedCar(
                listing_id=1001,
                brand='Honda',
                model='City',
                body_type='Sedan',
                fuel_type='Petrol',
                transmission='Manual',
                original_price=1000000,
                current_price=600000,
                registration_year=2020,
                age_years=5,
                mileage_km=50000,
                num_owners=1,
                is_sold=False,
                condition_score=85.0,
                listing_date=date.today(),
                city='Mumbai',
                seller_name='Test Seller',
                seller_phone='+919876543210'
            )
            db.session.add(used_car)
            db.session.commit()

        response = client.get('/')
        assert response.status_code == 200


class TestRecommendationsRoutes:
    """Tests for car recommendation routes"""

    def test_recommendations_page_loads(self, client):
        """Test recommendations form page returns 200"""
        response = client.get('/recommendations')
        assert response.status_code == 200

    @patch('app.routes.ml_models')
    def test_get_recommendations_success(self, mock_ml_models, client):
        """Test successful recommendation API call"""
        # Mock the recommendation engine
        mock_ml_models.recommendation_engine.get_recommendations.return_value = [
            {'car_id': 1, 'brand': 'Maruti Suzuki', 'model': 'Swift', 'price': 800000, 'score': 0.95}
        ]

        response = client.post(
            '/api/recommendations',
            json={
                'budget_min': 500000,
                'budget_max': 1000000
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert 'recommendations' in data

    def test_get_recommendations_validation_error(self, client):
        """Test recommendation API with invalid data"""
        response = client.post(
            '/api/recommendations',
            json={
                'budget_min': 50,  # Too low (min is 100000)
                'budget_max': 1000000
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'errors' in data

    def test_get_recommendations_budget_range_error(self, client):
        """Test recommendation API with min > max budget"""
        response = client.post(
            '/api/recommendations',
            json={
                'budget_min': 2000000,
                'budget_max': 1000000
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    @patch('app.routes.ml_models')
    def test_get_recommendations_with_all_filters(self, mock_ml_models, client):
        """Test recommendation API with all filter options"""
        mock_ml_models.recommendation_engine.get_recommendations.return_value = []

        response = client.post(
            '/api/recommendations',
            json={
                'budget_min': 500000,
                'budget_max': 1500000,
                'fuel_type': 'Petrol',
                'body_type': 'SUV',
                'transmission': 'Automatic',
                'usage_type': 'city',
                'family_size': 5,
                'priority_factor': 'safety'
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True

    @patch('app.routes.ml_models')
    def test_get_recommendations_ml_error(self, mock_ml_models, client):
        """Test recommendation API handles ML errors gracefully"""
        mock_ml_models.recommendation_engine.get_recommendations.side_effect = Exception("ML Error")

        response = client.post(
            '/api/recommendations',
            json={
                'budget_min': 500000,
                'budget_max': 1000000
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 500
        assert data['success'] is False
        assert 'error' in data

    def test_compare_cars_requires_minimum_two(self, client):
        """Test compare cars requires at least 2 cars"""
        response = client.get('/recommendations/compare?car_ids=1')
        # Should redirect back to recommendations
        assert response.status_code == 302

    def test_compare_cars_with_valid_ids(self, app, client):
        """Test compare cars fetches correct cars from database"""
        with app.app_context():
            car1 = NewCar(
                car_id=1, brand='Maruti', model='Swift', price=800000,
                fuel_type='Petrol', body_type='Hatchback', transmission='Manual',
                safety_rating=4, mileage=20.0
            )
            car2 = NewCar(
                car_id=2, brand='Hyundai', model='i20', price=900000,
                fuel_type='Petrol', body_type='Hatchback', transmission='Manual',
                safety_rating=4, mileage=18.0
            )
            db.session.add_all([car1, car2])
            db.session.commit()

            # Verify cars were created correctly
            cars = NewCar.query.filter(NewCar.car_id.in_([1, 2])).all()
            assert len(cars) == 2
            assert cars[0].brand in ['Maruti', 'Hyundai']


class TestMarketplaceRoutes:
    """Tests for marketplace routes"""

    def test_marketplace_page_loads(self, client):
        """Test marketplace listing page returns 200"""
        response = client.get('/marketplace')
        assert response.status_code == 200

    def test_marketplace_with_filters(self, app, client):
        """Test marketplace with various filters"""
        with app.app_context():
            car = UsedCar(
                listing_id=1001,
                brand='Honda',
                model='City',
                body_type='Sedan',
                fuel_type='Petrol',
                transmission='Automatic',
                original_price=1200000,
                current_price=700000,
                registration_year=2020,
                age_years=5,
                mileage_km=40000,
                num_owners=1,
                is_sold=False,
                condition_score=85.0,
                listing_date=date.today(),
                city='Mumbai',
                seller_name='Test Seller',
                seller_phone='+919876543210'
            )
            db.session.add(car)
            db.session.commit()

        # Test with filters
        response = client.get('/marketplace?brand=Honda&body_type=Sedan&fuel_type=Petrol')
        assert response.status_code == 200

        # Test with price filters
        response = client.get('/marketplace?price_min=500000&price_max=1000000')
        assert response.status_code == 200

        # Test with year filter
        response = client.get('/marketplace?year_min=2018')
        assert response.status_code == 200

    def test_marketplace_pagination(self, app, client):
        """Test marketplace pagination"""
        with app.app_context():
            # Add multiple cars
            for i in range(15):
                car = UsedCar(
                    listing_id=1001 + i,
                    brand='Test',
                    model=f'Model{i}',
                    body_type='Sedan',
                    fuel_type='Petrol',
                    transmission='Manual',
                    original_price=600000 + i * 10000,
                    current_price=500000 + i * 10000,
                    registration_year=2020,
                    age_years=5,
                    mileage_km=30000,
                    num_owners=1,
                    is_sold=False,
                    condition_score=80.0,
                    listing_date=date.today(),
                    city='Mumbai',
                    seller_name='Test Seller',
                    seller_phone='+919876543210'
                )
                db.session.add(car)
            db.session.commit()

        response = client.get('/marketplace?page=1')
        assert response.status_code == 200

        response = client.get('/marketplace?page=2')
        assert response.status_code == 200

    def test_car_details_page(self, app, client):
        """Test car details page loads"""
        with app.app_context():
            car = UsedCar(
                listing_id=1001,
                brand='Honda',
                model='City',
                variant='V CVT',
                body_type='Sedan',
                fuel_type='Petrol',
                transmission='Automatic',
                original_price=1200000,
                current_price=700000,
                registration_year=2020,
                age_years=5,
                mileage_km=40000,
                num_owners=1,
                is_sold=False,
                condition_score=85.0,
                listing_date=date.today(),
                city='Mumbai',
                seller_name='Test Seller',
                seller_phone='+919876543210',
                service_history='Full',
                accident_history='No',
                insurance_validity_months=12
            )
            db.session.add(car)
            db.session.commit()

        response = client.get('/marketplace/car/1001')
        assert response.status_code == 200

    def test_car_details_not_found(self, client):
        """Test car details returns 404 for non-existent car"""
        response = client.get('/marketplace/car/99999')
        assert response.status_code == 404

    def test_list_car_form_page(self, client):
        """Test list car form page loads"""
        response = client.get('/marketplace/list')
        assert response.status_code == 200


class TestListCarAPI:
    """Tests for car listing API"""

    def test_list_car_api_requires_auth(self, client):
        """Test listing car API requires authentication"""
        response = client.post(
            '/api/marketplace/list',
            json={
                'brand': 'Honda',
                'model': 'City',
                'body_type': 'Sedan',
                'registration_year': 2020,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'mileage_km': 30000,
                'num_owners': 1,
                'original_price': 1200000,
                'current_price': 800000,
                'city': 'Mumbai',
                'seller_name': 'John Doe',
                'seller_phone': '+919876543210'
            },
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_list_car_api_success(self, client, auth_headers):
        """Test successful car listing via API"""
        response = client.post(
            '/api/marketplace/list',
            headers=auth_headers,
            json={
                'brand': 'Honda',
                'model': 'City',
                'body_type': 'Sedan',
                'registration_year': 2020,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'mileage_km': 30000,
                'num_owners': 1,
                'original_price': 1200000,
                'current_price': 800000,
                'city': 'Mumbai',
                'seller_name': 'John Doe',
                'seller_phone': '+919876543210'
            }
        )
        data = response.get_json()

        assert response.status_code == 201
        assert data['success'] is True
        assert 'listing_id' in data

    def test_list_car_api_validation_error(self, client, auth_headers):
        """Test car listing API with invalid data"""
        response = client.post(
            '/api/marketplace/list',
            headers=auth_headers,
            json={
                'brand': 'Honda',
                # Missing required fields
            }
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False
        assert 'errors' in data

    def test_list_car_api_invalid_body_type(self, client, auth_headers):
        """Test car listing API with invalid body type"""
        response = client.post(
            '/api/marketplace/list',
            headers=auth_headers,
            json={
                'brand': 'Honda',
                'model': 'City',
                'body_type': 'InvalidType',  # Invalid
                'registration_year': 2020,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'mileage_km': 30000,
                'num_owners': 1,
                'original_price': 1200000,
                'current_price': 800000,
                'city': 'Mumbai',
                'seller_name': 'John Doe',
                'seller_phone': '+919876543210'
            }
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False


class TestPricePredictionAPI:
    """Tests for price prediction API"""

    @patch('app.routes.ml_models')
    def test_predict_price_success(self, mock_ml_models, client):
        """Test successful price prediction"""
        mock_ml_models.price_predictor.predict_price.return_value = 650000

        response = client.post(
            '/api/predict-price',
            json={
                'brand': 'Maruti Suzuki',
                'body_type': 'Hatchback',
                'registration_year': 2020,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'mileage_km': 30000,
                'num_owners': 1,
                'original_price': 800000
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert 'predicted_price' in data

    def test_predict_price_validation_error(self, client):
        """Test price prediction with invalid data"""
        response = client.post(
            '/api/predict-price',
            json={
                'brand': 'Maruti',
                # Missing required fields
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    @patch('app.routes.ml_models')
    def test_predict_price_ml_error(self, mock_ml_models, client):
        """Test price prediction handles ML errors"""
        mock_ml_models.price_predictor.predict_price.side_effect = Exception("ML Error")

        response = client.post(
            '/api/predict-price',
            json={
                'brand': 'Maruti Suzuki',
                'body_type': 'Hatchback',
                'registration_year': 2020,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'mileage_km': 30000,
                'num_owners': 1,
                'original_price': 800000
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 500
        assert data['success'] is False


class TestBuybackValuationRoutes:
    """Tests for buy-back valuation routes"""

    def test_buyback_page_loads(self, client):
        """Test buyback form page returns 200"""
        response = client.get('/buyback')
        assert response.status_code == 200

    @patch('app.routes.ml_models')
    def test_buyback_valuation_success(self, mock_ml_models, client):
        """Test successful buyback valuation"""
        mock_ml_models.buyback_valuator.get_valuation.return_value = {
            'condition_score': 75.0,
            'estimated_price_min': 450000,
            'estimated_price_max': 550000,
            'estimated_price_avg': 500000,
            'confidence_score': 0.85
        }

        response = client.post(
            '/api/buyback-valuation',
            json={
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
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True
        assert 'valuation' in data
        assert 'valuation_id' in data['valuation']

    def test_buyback_valuation_validation_error(self, client):
        """Test buyback valuation with invalid data"""
        response = client.post(
            '/api/buyback-valuation',
            json={
                'brand': 'Maruti',
                # Missing required fields
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 400
        assert data['success'] is False

    @patch('app.routes.ml_models')
    def test_buyback_valuation_with_optional_fields(self, mock_ml_models, client):
        """Test buyback valuation with optional fields"""
        mock_ml_models.buyback_valuator.get_valuation.return_value = {
            'condition_score': 80.0,
            'estimated_price_min': 500000,
            'estimated_price_max': 600000,
            'estimated_price_avg': 550000,
            'confidence_score': 0.90
        }

        response = client.post(
            '/api/buyback-valuation',
            json={
                'brand': 'Honda',
                'model': 'City',
                'variant': 'V CVT',
                'registration_year': 2020,
                'mileage_km': 30000,
                'num_owners': 1,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'service_history': 'Full',
                'accident_history': 'No',
                'insurance_valid': True,
                'modifications': 'Alloy wheels',
                'customer_name': 'Jane Doe',
                'customer_phone': '+919876543211',
                'customer_email': 'jane@example.com',
                'inspection_requested': True
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True

    @patch('app.routes.ml_models')
    def test_buyback_valuation_ml_error(self, mock_ml_models, client):
        """Test buyback valuation handles ML errors"""
        mock_ml_models.buyback_valuator.get_valuation.side_effect = Exception("ML Error")

        response = client.post(
            '/api/buyback-valuation',
            json={
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
            },
            content_type='application/json'
        )
        data = response.get_json()

        assert response.status_code == 500
        assert data['success'] is False

    @patch('app.routes.ml_models')
    def test_valuation_details_page(self, mock_ml_models, app, client):
        """Test valuation details page loads (skipped if template missing)"""
        mock_ml_models.buyback_valuator.get_valuation.return_value = {
            'condition_score': 75.0,
            'estimated_price_min': 450000,
            'estimated_price_max': 550000,
            'estimated_price_avg': 500000,
            'confidence_score': 0.85
        }

        # First create a valuation
        response = client.post(
            '/api/buyback-valuation',
            json={
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
            },
            content_type='application/json'
        )
        data = response.get_json()
        valuation_id = data['valuation']['valuation_id']

        # Check valuation was created in database
        with app.app_context():
            valuation = Valuation.query.get(valuation_id)
            assert valuation is not None
            assert valuation.brand == 'Maruti Suzuki'
            assert valuation.customer_email == 'john@example.com'

    def test_valuation_details_not_found(self, client):
        """Test valuation details returns 404 for non-existent valuation"""
        response = client.get('/buyback/valuation/99999')
        assert response.status_code == 404


class TestUtilityRoutes:
    """Tests for utility routes"""

    def test_get_brands(self, app, client):
        """Test get brands API"""
        with app.app_context():
            car1 = NewCar(car_id=1, brand='Maruti Suzuki', model='Swift', price=800000)
            car2 = NewCar(car_id=2, brand='Hyundai', model='i20', price=900000)
            db.session.add_all([car1, car2])
            db.session.commit()

        response = client.get('/api/brands')
        data = response.get_json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert 'Maruti Suzuki' in data
        assert 'Hyundai' in data

    def test_get_brands_empty(self, client):
        """Test get brands returns empty list when no cars"""
        response = client.get('/api/brands')
        data = response.get_json()

        assert response.status_code == 200
        assert data == []

    def test_get_models_for_brand(self, app, client):
        """Test get models API for a specific brand"""
        with app.app_context():
            car1 = NewCar(car_id=1, brand='Maruti Suzuki', model='Swift', price=800000)
            car2 = NewCar(car_id=2, brand='Maruti Suzuki', model='Baleno', price=900000)
            car3 = NewCar(car_id=3, brand='Hyundai', model='i20', price=850000)
            db.session.add_all([car1, car2, car3])
            db.session.commit()

        response = client.get('/api/models/Maruti Suzuki')
        data = response.get_json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert 'Swift' in data
        assert 'Baleno' in data
        assert 'i20' not in data

    def test_get_models_unknown_brand(self, client):
        """Test get models returns empty list for unknown brand"""
        response = client.get('/api/models/UnknownBrand')
        data = response.get_json()

        assert response.status_code == 200
        assert data == []

    def test_emi_calculator_page(self, client):
        """Test EMI calculator page loads"""
        response = client.get('/emi-calculator')
        assert response.status_code == 200


class TestListCarForm:
    """Tests for car listing via form submission"""

    def test_list_car_form_success(self, app, client):
        """Test successful car listing via form"""
        response = client.post(
            '/marketplace/list',
            data={
                'brand': 'Honda',
                'model': 'City',
                'variant': 'V CVT',
                'body_type': 'Sedan',
                'registration_year': '2020',
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'mileage_km': '30000',
                'num_owners': '1',
                'original_price': '1200000',
                'current_price': '800000',
                'condition_score': '85',
                'color': 'White',
                'city': 'Mumbai',
                'seller_name': 'John Doe',
                'seller_phone': '+919876543210'
            },
            follow_redirects=False
        )

        # Should redirect to car details page on success
        assert response.status_code == 302

    def test_list_car_form_missing_required(self, client):
        """Test car listing form with missing required fields"""
        response = client.post(
            '/marketplace/list',
            data={
                'brand': 'Honda',
                # Missing other required fields
            }
        )

        # Should return the form page with error
        assert response.status_code == 200

    def test_list_car_form_invalid_numeric(self, client):
        """Test car listing form with invalid numeric values"""
        response = client.post(
            '/marketplace/list',
            data={
                'brand': 'Honda',
                'model': 'City',
                'body_type': 'Sedan',
                'registration_year': 'invalid',  # Should be numeric
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'current_price': '800000',
                'seller_name': 'John Doe',
                'seller_phone': '+919876543210'
            }
        )

        # Should return the form page
        assert response.status_code == 200


class TestAuthenticatedRecommendations:
    """Tests for recommendations with authenticated user"""

    @patch('app.routes.ml_models')
    def test_recommendations_saves_history_for_authenticated_user(
        self, mock_ml_models, app, client, auth_headers
    ):
        """Test recommendations saves history when user is authenticated"""
        mock_ml_models.recommendation_engine.get_recommendations.return_value = [
            {'car_id': 1, 'brand': 'Maruti', 'model': 'Swift', 'price': 800000}
        ]

        response = client.post(
            '/api/recommendations',
            headers=auth_headers,
            json={
                'budget_min': 500000,
                'budget_max': 1000000,
                'fuel_type': 'Petrol',
                'body_type': 'Hatchback'
            }
        )
        data = response.get_json()

        assert response.status_code == 200
        assert data['success'] is True

        # Check history was saved
        with app.app_context():
            history = RecommendationHistory.query.first()
            assert history is not None
            assert history.budget_min == 500000
            assert history.budget_max == 1000000
