"""
Buy-back valuation model
Uses the price prediction model with depreciation calculations
"""
import pandas as pd
import numpy as np
import joblib
import os

class BuyBackValuator:
    """Class for buy-back car valuation"""

    def __init__(self, models_dir='trained_models'):
        """Initialize by loading the trained price prediction model"""
        self.models_dir = models_dir

        # Load the best model (XGBoost)
        model_path = os.path.join(models_dir, 'xgboost_price_prediction.pkl')
        self.model = joblib.load(model_path)

        # Load label encoders and scaler
        self.label_encoders = joblib.load(os.path.join(models_dir, 'price_label_encoders.pkl'))
        self.scaler = joblib.load(os.path.join(models_dir, 'price_scaler.pkl'))
        self.feature_names = joblib.load(os.path.join(models_dir, 'price_feature_names.pkl'))

        print("Buy-back valuation model loaded successfully!")

    def calculate_depreciation(self, original_price, age_years, condition_factor=1.0):
        """
        Calculate depreciated price based on age
        Year 1: 15-20%
        Year 2-5: 10-15% per year
        Year 6+: 5-10% per year
        """
        depreciation = 0

        if age_years >= 1:
            depreciation += 0.175  # First year average

        if age_years > 1:
            for year in range(2, min(age_years + 1, 6)):
                depreciation += 0.125  # Years 2-5 average

        if age_years > 5:
            for year in range(6, age_years + 1):
                depreciation += 0.075  # Year 6+ average

        # Adjust for condition
        depreciation = depreciation * condition_factor

        # Calculate current value
        current_value = original_price * (1 - min(depreciation, 0.75))  # Max 75% depreciation

        return current_value

    def calculate_condition_score(self, age_years, mileage_km, num_owners,
                                 service_history, accident_history):
        """Calculate condition score based on various factors"""
        base_score = 100

        # Age factor
        age_penalty = age_years * 4

        # Mileage factor (assuming 12000 km/year is average)
        expected_mileage = age_years * 12000
        if mileage_km > expected_mileage:
            mileage_penalty = ((mileage_km - expected_mileage) / expected_mileage) * 10
        else:
            mileage_penalty = 0

        # Owner factor
        owner_penalty = (num_owners - 1) * 6

        # Service history factor
        service_penalty = {'Complete': 0, 'Partial': 10, 'Unknown': 15}.get(service_history, 10)

        # Accident history factor
        accident_penalty = {'No': 0, 'Minor': 15, 'Major': 30}.get(accident_history, 10)

        # Calculate final score
        condition_score = base_score - age_penalty - mileage_penalty - owner_penalty - service_penalty - accident_penalty
        condition_score = max(40, min(95, condition_score))

        return round(condition_score, 1)

    def get_valuation(self, car_details):
        """
        Get buy-back valuation for a car

        Parameters:
        -----------
        car_details : dict
            Dictionary containing car details:
            - brand: str
            - model: str (not used in prediction, but for reference)
            - body_type: str
            - registration_year: int
            - mileage_km: int
            - num_owners: int
            - fuel_type: str
            - transmission: str
            - original_price: int
            - service_history: str ('Complete', 'Partial', 'Unknown')
            - accident_history: str ('No', 'Minor', 'Major')
            - insurance_validity_months: int
            - seating_capacity: int
            - engine_cc: int
            - fuel_efficiency_kmpl: float

        Returns:
        --------
        dict: Valuation results with min, max, average prices and confidence score
        """
        current_year = 2025
        age_years = current_year - car_details['registration_year']

        # Calculate condition score
        condition_score = self.calculate_condition_score(
            age_years,
            car_details['mileage_km'],
            car_details['num_owners'],
            car_details['service_history'],
            car_details['accident_history']
        )

        # Calculate average km per year
        avg_km_per_year = car_details['mileage_km'] / max(age_years, 1)

        # Prepare features for prediction
        features = {
            'brand': car_details['brand'],
            'body_type': car_details['body_type'],
            'registration_year': car_details['registration_year'],
            'age_years': age_years,
            'fuel_type': car_details['fuel_type'],
            'transmission': car_details['transmission'],
            'mileage_km': car_details['mileage_km'],
            'num_owners': car_details['num_owners'],
            'original_price': car_details['original_price'],
            'condition_score': condition_score,
            'insurance_validity_months': car_details.get('insurance_validity_months', 0),
            'service_history': car_details['service_history'],
            'accident_history': car_details['accident_history'],
            'seating_capacity': car_details.get('seating_capacity', 5),
            'engine_cc': car_details.get('engine_cc', 1200),
            'fuel_efficiency_kmpl': car_details.get('fuel_efficiency_kmpl', 15.0),
            'avg_km_per_year': avg_km_per_year
        }

        # Create DataFrame with features in correct order
        X = pd.DataFrame([features])

        # Encode categorical variables
        categorical_columns = ['brand', 'body_type', 'fuel_type', 'transmission',
                              'service_history', 'accident_history']

        for col in categorical_columns:
            if col in self.label_encoders:
                # Handle unknown categories
                try:
                    X[col] = self.label_encoders[col].transform(X[col].astype(str))
                except ValueError:
                    # If category not seen during training, use most common category
                    X[col] = 0

        # Ensure features are in the correct order
        X = X[self.feature_names]

        # Scale features
        X_scaled = self.scaler.transform(X)

        # Make prediction
        predicted_price = self.model.predict(X_scaled)[0]

        # Calculate price range (typically ±10% for buy-back offers)
        price_variance = 0.10
        min_price = predicted_price * (1 - price_variance)
        max_price = predicted_price * (1 + price_variance)

        # Adjust based on condition score
        if condition_score < 50:
            min_price *= 0.85
            max_price *= 0.90
            confidence = 0.65
        elif condition_score < 65:
            min_price *= 0.90
            max_price *= 0.95
            confidence = 0.75
        elif condition_score < 80:
            min_price *= 0.95
            max_price *= 1.00
            confidence = 0.85
        else:
            min_price *= 1.00
            max_price *= 1.05
            confidence = 0.92

        # Apply market demand adjustments (simplified)
        # In production, this would use real market data
        market_factor = 1.0
        if age_years <= 3:
            market_factor = 1.05  # Higher demand for newer cars
        elif age_years > 10:
            market_factor = 0.92  # Lower demand for older cars

        min_price *= market_factor
        max_price *= market_factor
        predicted_price *= market_factor

        # Depreciation-based estimate for comparison
        depreciation_estimate = self.calculate_depreciation(
            car_details['original_price'],
            age_years,
            condition_score / 100
        )

        # Final price is weighted average of model prediction and depreciation
        final_min = int(min_price * 0.7 + depreciation_estimate * 0.85 * 0.3)
        final_max = int(max_price * 0.7 + depreciation_estimate * 1.05 * 0.3)
        final_avg = int((final_min + final_max) / 2)

        # Ensure logical ordering
        final_min = min(final_min, final_avg, final_max)
        final_max = max(final_min, final_avg, final_max)

        return {
            'estimated_price_min': final_min,
            'estimated_price_max': final_max,
            'estimated_price_avg': final_avg,
            'condition_score': condition_score,
            'confidence_score': round(confidence, 2),
            'depreciation_percent': round((1 - (final_avg / car_details['original_price'])) * 100, 1),
            'market_trend': 'Good' if market_factor > 1.0 else 'Fair' if market_factor == 1.0 else 'Low',
            'recommendation': self._get_recommendation(condition_score, age_years)
        }

    def _get_recommendation(self, condition_score, age_years):
        """Generate recommendation based on valuation"""
        if condition_score >= 75 and age_years <= 5:
            return "Excellent condition! Great time to sell with high resale value."
        elif condition_score >= 60 and age_years <= 8:
            return "Good condition. Fair resale value expected."
        elif age_years > 10:
            return "Older vehicle. Consider maintenance costs vs. selling price."
        else:
            return "Vehicle condition may affect resale value. Service recommended before sale."


def test_valuation():
    """Test the buy-back valuation model"""
    print("Testing Buy-Back Valuation Model...")
    print("="*50)

    valuator = BuyBackValuator()

    # Test case 1: 5-year-old Hyundai Creta
    test_car = {
        'brand': 'Hyundai',
        'model': 'Creta',
        'body_type': 'SUV',
        'registration_year': 2020,
        'mileage_km': 50000,
        'num_owners': 1,
        'fuel_type': 'Petrol',
        'transmission': 'Manual',
        'original_price': 1200000,
        'service_history': 'Complete',
        'accident_history': 'No',
        'insurance_validity_months': 8,
        'seating_capacity': 5,
        'engine_cc': 1500,
        'fuel_efficiency_kmpl': 16.0
    }

    print("\nTest Car Details:")
    print(f"Brand: {test_car['brand']} {test_car['model']}")
    print(f"Year: {test_car['registration_year']}")
    print(f"Mileage: {test_car['mileage_km']:,} km")
    print(f"Original Price: Rs {test_car['original_price']:,}")
    print(f"Owners: {test_car['num_owners']}")
    print(f"Service: {test_car['service_history']}")
    print(f"Accident: {test_car['accident_history']}")

    valuation = valuator.get_valuation(test_car)

    print("\nValuation Results:")
    print(f"Estimated Price Range: Rs {valuation['estimated_price_min']:,} - Rs {valuation['estimated_price_max']:,}")
    print(f"Average Estimate: Rs {valuation['estimated_price_avg']:,}")
    print(f"Condition Score: {valuation['condition_score']}/100")
    print(f"Confidence: {valuation['confidence_score']*100:.0f}%")
    print(f"Depreciation: {valuation['depreciation_percent']}%")
    print(f"Market Trend: {valuation['market_trend']}")
    print(f"Recommendation: {valuation['recommendation']}")

    print("\n" + "="*50)
    print("Buy-back valuation model test completed!")


if __name__ == '__main__':
    test_valuation()
