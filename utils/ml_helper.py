"""
ML Helper functions for loading and using trained models
"""
import joblib
import pandas as pd
import numpy as np
import os
import sys

# Add models directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))

from buyback_valuation_model import BuyBackValuator as BBValuator

class RecommendationEngine:
    """Helper class for car recommendations"""

    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained_models')

        # Load the best model (XGBoost)
        self.model = joblib.load(os.path.join(models_dir, 'xgboost_recommendation.pkl'))
        self.label_encoders = joblib.load(os.path.join(models_dir, 'label_encoders.pkl'))
        self.scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))

        print("Recommendation engine loaded successfully!")

    def get_recommendations(self, preferences, top_n=5):
        """
        Get car recommendations based on user preferences

        Parameters:
        -----------
        preferences : dict
            User preferences including budget, fuel type, etc.
        top_n : int
            Number of recommendations to return

        Returns:
        --------
        list of dicts with recommended cars
        """
        from app.models import NewCar

        # Build query based on preferences
        query = NewCar.query

        # Budget filter
        if preferences.get('budget_min'):
            query = query.filter(NewCar.price >= preferences['budget_min'])
        if preferences.get('budget_max'):
            query = query.filter(NewCar.price <= preferences['budget_max'])

        # Fuel type filter
        if preferences.get('fuel_type') and preferences['fuel_type'] != 'any':
            query = query.filter(NewCar.fuel_type == preferences['fuel_type'])

        # Body type filter
        if preferences.get('body_type') and preferences['body_type'] != 'any':
            query = query.filter(NewCar.body_type == preferences['body_type'])

        # Transmission filter
        if preferences.get('transmission') and preferences['transmission'] != 'any':
            query = query.filter(NewCar.transmission == preferences['transmission'])

        # Seating capacity (based on family size)
        if preferences.get('family_size'):
            required_seats = preferences['family_size']
            query = query.filter(NewCar.seating_capacity >= required_seats)

        # Get all matching cars
        matching_cars = query.all()

        if not matching_cars:
            return []

        # Calculate scores based on priority factor
        priority = preferences.get('priority_factor', 'overall')
        usage_type = preferences.get('usage_type', 'mixed')

        scored_cars = []
        for car in matching_cars:
            score = 0

            if priority == 'mileage':
                score = car.mileage_score * 0.60 + car.safety_score * 0.20 + car.comfort_score * 0.20
            elif priority == 'performance':
                score = car.performance_score * 0.60 + car.safety_score * 0.25 + car.comfort_score * 0.15
            elif priority == 'safety':
                score = car.safety_score * 0.60 + car.comfort_score * 0.25 + car.mileage_score * 0.15
            elif priority == 'comfort':
                score = car.comfort_score * 0.60 + car.safety_score * 0.25 + car.mileage_score * 0.15
            else:  # overall
                score = (car.mileage_score * 0.25 + car.performance_score * 0.20 +
                        car.safety_score * 0.30 + car.comfort_score * 0.25)

            # Adjust for usage type
            if usage_type == 'city':
                score = score * 0.7 + car.city_suitability_score * 0.3
            elif usage_type == 'highway':
                score = score * 0.7 + car.highway_suitability_score * 0.3
            else:  # mixed
                score = score * 0.7 + (car.city_suitability_score + car.highway_suitability_score) / 2 * 0.3

            scored_cars.append({
                'car': car,
                'score': score,
                'confidence': min(95, score * 10)  # Convert to percentage
            })

        # Sort by score and get top N
        scored_cars.sort(key=lambda x: x['score'], reverse=True)
        top_recommendations = scored_cars[:top_n]

        # Format results
        results = []
        for item in top_recommendations:
            car = item['car']
            results.append({
                'car_id': car.car_id,
                'brand': car.brand,
                'model': car.model,
                'variant': car.variant,
                'price': car.price,
                'fuel_type': car.fuel_type,
                'mileage': car.mileage,
                'transmission': car.transmission,
                'body_type': car.body_type,
                'seating_capacity': car.seating_capacity,
                'safety_rating': car.safety_rating,
                'power_hp': car.power_hp,
                'resale_value_3yr_percent': car.resale_value_3yr_percent,
                'resale_value_5yr_percent': car.resale_value_5yr_percent,
                'maintenance_cost_annual': car.maintenance_cost_annual,
                'score': round(item['score'], 2),
                'confidence': round(item['confidence'], 1)
            })

        return results


class PricePredictor:
    """Helper class for price prediction"""

    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained_models')

        # Load the best model (XGBoost)
        self.model = joblib.load(os.path.join(models_dir, 'xgboost_price_prediction.pkl'))
        self.label_encoders = joblib.load(os.path.join(models_dir, 'price_label_encoders.pkl'))
        self.scaler = joblib.load(os.path.join(models_dir, 'price_scaler.pkl'))
        self.feature_names = joblib.load(os.path.join(models_dir, 'price_feature_names.pkl'))

        print("Price predictor loaded successfully!")

    def predict_price(self, car_details):
        """
        Predict price for a used car

        Parameters:
        -----------
        car_details : dict
            Dictionary with car details

        Returns:
        --------
        float: predicted price
        """
        current_year = 2025
        age_years = current_year - car_details.get('registration_year', 2020)

        # Calculate average km per year
        mileage_km = car_details.get('mileage_km', 50000)
        avg_km_per_year = mileage_km / max(age_years, 1)

        # Prepare features
        features = {
            'brand': car_details.get('brand', 'Maruti Suzuki'),
            'body_type': car_details.get('body_type', 'Hatchback'),
            'registration_year': car_details.get('registration_year', 2020),
            'age_years': age_years,
            'fuel_type': car_details.get('fuel_type', 'Petrol'),
            'transmission': car_details.get('transmission', 'Manual'),
            'mileage_km': mileage_km,
            'num_owners': car_details.get('num_owners', 1),
            'original_price': car_details.get('original_price', 600000),
            'condition_score': car_details.get('condition_score', 70),
            'insurance_validity_months': car_details.get('insurance_validity_months', 6),
            'service_history': car_details.get('service_history', 'Partial'),
            'accident_history': car_details.get('accident_history', 'No'),
            'seating_capacity': car_details.get('seating_capacity', 5),
            'engine_cc': car_details.get('engine_cc', 1200),
            'fuel_efficiency_kmpl': car_details.get('fuel_efficiency_kmpl', 15.0),
            'avg_km_per_year': avg_km_per_year
        }

        # Create DataFrame
        X = pd.DataFrame([features])

        # Encode categorical variables
        categorical_columns = ['brand', 'body_type', 'fuel_type', 'transmission',
                              'service_history', 'accident_history']

        for col in categorical_columns:
            if col in self.label_encoders:
                try:
                    X[col] = self.label_encoders[col].transform(X[col].astype(str))
                except ValueError:
                    X[col] = 0  # Unknown category

        # Ensure features are in correct order
        X = X[self.feature_names]

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Predict
        predicted_price = self.model.predict(X_scaled)[0]

        return predicted_price


class BuyBackValuator:
    """Wrapper for buy-back valuation"""

    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'trained_models')
        self.valuator = BBValuator(models_dir)

        print("Buy-back valuator loaded successfully!")

    def get_valuation(self, car_details):
        """Get buy-back valuation"""
        return self.valuator.get_valuation(car_details)
