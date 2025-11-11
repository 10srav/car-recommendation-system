"""
Script to generate synthetic used cars dataset for Indian automotive marketplace
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Load new cars data to base used cars on realistic models
# For standalone execution, we'll define the car models here
CAR_MODELS = {
    'Maruti Suzuki': ['Alto', 'Swift', 'Baleno', 'Dzire', 'Brezza', 'Ertiga', 'WagonR', 'Celerio', 'Ciaz', 'XL6'],
    'Hyundai': ['i10', 'i20', 'Grand i10', 'Aura', 'Verna', 'Venue', 'Creta', 'Alcazar'],
    'Tata': ['Tiago', 'Altroz', 'Tigor', 'Punch', 'Nexon', 'Harrier', 'Safari'],
    'Mahindra': ['XUV300', 'XUV700', 'Scorpio', 'Thar', 'Bolero', 'XUV500'],
    'Honda': ['Jazz', 'Amaze', 'City', 'Civic', 'WR-V'],
    'Toyota': ['Glanza', 'Fortuner', 'Innova Crysta', 'Urban Cruiser'],
    'Kia': ['Sonet', 'Seltos', 'Carens'],
    'Ford': ['EcoSport', 'Endeavour', 'Figo', 'Aspire'],  # Used models
    'Volkswagen': ['Polo', 'Vento', 'Taigun', 'Tiguan'],
    'Renault': ['Kwid', 'Kiger', 'Duster', 'Triber']
}

FUEL_TYPES = ['Petrol', 'Diesel', 'CNG', 'Electric']
TRANSMISSIONS = ['Manual', 'Automatic', 'AMT', 'CVT']
BODY_TYPES = ['Hatchback', 'Sedan', 'SUV', 'MPV']
COLORS = ['White', 'Silver', 'Black', 'Red', 'Blue', 'Grey', 'Brown', 'Orange']

# Cities in India
CITIES = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad',
          'Jaipur', 'Lucknow', 'Chandigarh', 'Indore', 'Kochi', 'Coimbatore', 'Nagpur']

def calculate_depreciation(original_price, age_years, condition_score):
    """
    Calculate depreciated price based on age and condition
    Year 1: 15-20%
    Year 2-5: 10-15% per year
    Year 6+: 5-10% per year
    """
    depreciation = 0

    if age_years >= 1:
        depreciation += random.uniform(0.15, 0.20)  # First year

    if age_years > 1:
        for year in range(2, min(age_years + 1, 6)):
            depreciation += random.uniform(0.10, 0.15)

    if age_years > 5:
        for year in range(6, age_years + 1):
            depreciation += random.uniform(0.05, 0.10)

    # Adjust for condition
    condition_factor = condition_score / 100
    depreciation = depreciation * (1.5 - condition_factor * 0.5)

    # Calculate current price
    current_price = original_price * (1 - min(depreciation, 0.75))  # Max 75% depreciation

    return int(current_price)

def generate_condition_score(age_years, mileage_km, num_owners):
    """Generate condition score based on various factors"""
    base_score = 100

    # Age factor
    age_penalty = age_years * random.uniform(3, 5)

    # Mileage factor (assuming 12000 km/year is average)
    expected_mileage = age_years * 12000
    if mileage_km > expected_mileage:
        mileage_penalty = ((mileage_km - expected_mileage) / expected_mileage) * 10
    else:
        mileage_penalty = 0

    # Owner factor
    owner_penalty = (num_owners - 1) * random.uniform(5, 8)

    # Calculate final score
    condition_score = base_score - age_penalty - mileage_penalty - owner_penalty
    condition_score = max(40, min(95, condition_score))  # Clamp between 40-95

    return round(condition_score, 1)

def generate_used_cars_dataset(num_records=600):
    """Generate synthetic used cars dataset"""

    data = []
    listing_id = 1

    current_year = 2025

    for _ in range(num_records):
        # Select random brand and model
        brand = random.choice(list(CAR_MODELS.keys()))
        model = random.choice(CAR_MODELS[brand])

        # Registration year (2010-2024)
        reg_year = random.randint(2010, 2024)
        age_years = current_year - reg_year

        # Determine body type based on model name
        if any(x in model.lower() for x in ['alto', 'swift', 'baleno', 'i10', 'i20', 'polo', 'jazz', 'tiago', 'altroz', 'kwid', 'figo']):
            body_type = 'Hatchback'
        elif any(x in model.lower() for x in ['dzire', 'amaze', 'city', 'verna', 'ciaz', 'aspire', 'vento', 'tigor', 'aura']):
            body_type = 'Sedan'
        elif any(x in model.lower() for x in ['ertiga', 'innova', 'carens', 'marazzo', 'xl6']):
            body_type = 'MPV'
        else:
            body_type = 'SUV'

        # Fuel type
        if body_type == 'SUV' and random.random() > 0.5:
            fuel_type = 'Diesel'
        elif random.random() > 0.8:
            fuel_type = random.choice(['CNG', 'Diesel'])
        else:
            fuel_type = 'Petrol'

        # Transmission
        if reg_year >= 2020:
            transmission = random.choice(['Manual', 'Manual', 'Automatic', 'AMT'])
        else:
            transmission = random.choice(['Manual', 'Manual', 'Manual', 'Automatic'])

        # Mileage driven
        avg_yearly_km = random.randint(8000, 18000)
        mileage_km = age_years * avg_yearly_km + random.randint(-5000, 5000)
        mileage_km = max(1000, mileage_km)

        # Number of owners
        if age_years <= 2:
            num_owners = 1
        elif age_years <= 5:
            num_owners = random.choice([1, 1, 2])
        elif age_years <= 10:
            num_owners = random.choice([1, 2, 2, 3])
        else:
            num_owners = random.choice([2, 3, 3, 4])

        # Original price (when new)
        if body_type == 'Hatchback':
            original_price = random.randint(400000, 900000)
        elif body_type == 'Sedan':
            original_price = random.randint(600000, 1500000)
        elif body_type == 'SUV':
            original_price = random.randint(800000, 3500000)
        else:  # MPV
            original_price = random.randint(800000, 2500000)

        # Condition score
        condition_score = generate_condition_score(age_years, mileage_km, num_owners)

        # Current price (depreciated)
        current_price = calculate_depreciation(original_price, age_years, condition_score)

        # Add some randomness to price
        current_price = int(current_price * random.uniform(0.95, 1.05))

        # Insurance validity (months remaining)
        insurance_validity = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

        # Service history (complete/partial/unknown)
        if num_owners == 1 and age_years <= 5:
            service_history = random.choice(['Complete', 'Complete', 'Partial'])
        else:
            service_history = random.choice(['Complete', 'Partial', 'Partial', 'Unknown'])

        # Accident history
        accident_history = random.choice(['No', 'No', 'No', 'Minor', 'Minor', 'Major'])

        # Color
        color = random.choice(COLORS)

        # Location
        city = random.choice(CITIES)

        # Seating capacity
        if body_type == 'Hatchback':
            seating = 5
        elif body_type == 'Sedan':
            seating = 5
        elif body_type == 'MPV':
            seating = random.choice([7, 8])
        else:
            seating = random.choice([5, 7])

        # Engine capacity
        if body_type == 'Hatchback':
            engine_cc = random.choice([800, 1000, 1200])
        elif body_type == 'Sedan':
            engine_cc = random.choice([1200, 1500, 1600])
        else:
            engine_cc = random.choice([1500, 2000, 2200, 2500])

        # Fuel efficiency (km/l)
        if fuel_type == 'Petrol':
            fuel_efficiency = round(random.uniform(12, 20), 1)
        elif fuel_type == 'Diesel':
            fuel_efficiency = round(random.uniform(15, 25), 1)
        elif fuel_type == 'CNG':
            fuel_efficiency = round(random.uniform(18, 28), 1)
        else:
            fuel_efficiency = round(random.uniform(12, 18), 1)

        # Registration state
        reg_state = city  # Simplified

        # RTO registered
        rto_codes = ['MH01', 'DL01', 'KA01', 'TN01', 'UP32', 'HR26', 'GJ01', 'RJ14', 'MP09']
        rto = random.choice(rto_codes)

        # Features present (as comma-separated string)
        features_list = []
        if random.random() > 0.3:
            features_list.append('Power Windows')
        if random.random() > 0.4:
            features_list.append('AC')
        if random.random() > 0.5:
            features_list.append('Power Steering')
        if random.random() > 0.6 and reg_year >= 2018:
            features_list.append('ABS')
        if random.random() > 0.7 and reg_year >= 2019:
            features_list.append('Airbags')
        if random.random() > 0.8 and current_price > 500000:
            features_list.append('Touchscreen Infotainment')
        if random.random() > 0.85 and current_price > 800000:
            features_list.append('Sunroof')

        features = ', '.join(features_list) if features_list else 'Basic'

        # Contact info (dummy)
        seller_name = f"Seller_{listing_id}"
        seller_phone = f"+91-{''.join([str(random.randint(0,9)) for _ in range(10)])}"

        # Listing date (within last 60 days)
        listing_date = datetime.now() - timedelta(days=random.randint(1, 60))
        listing_date_str = listing_date.strftime('%Y-%m-%d')

        # Negotiable
        negotiable = random.choice(['Yes', 'No', 'No'])  # More likely to be non-negotiable

        # Test drive available
        test_drive = random.choice(['Yes', 'Yes', 'No'])

        # Create record
        record = {
            'listing_id': listing_id,
            'brand': brand,
            'model': model,
            'variant': random.choice(['Base', 'Mid', 'Top', 'VXI', 'ZXI', 'LXI']),
            'body_type': body_type,
            'registration_year': reg_year,
            'age_years': age_years,
            'fuel_type': fuel_type,
            'transmission': transmission,
            'mileage_km': mileage_km,
            'num_owners': num_owners,
            'original_price': original_price,
            'current_price': current_price,
            'condition_score': condition_score,
            'insurance_validity_months': insurance_validity,
            'service_history': service_history,
            'accident_history': accident_history,
            'color': color,
            'seating_capacity': seating,
            'engine_cc': engine_cc,
            'fuel_efficiency_kmpl': fuel_efficiency,
            'rto': rto,
            'city': city,
            'features': features,
            'seller_name': seller_name,
            'seller_phone': seller_phone,
            'listing_date': listing_date_str,
            'negotiable': negotiable,
            'test_drive_available': test_drive
        }

        data.append(record)
        listing_id += 1

    # Create DataFrame
    df = pd.DataFrame(data)

    return df

if __name__ == '__main__':
    print("Generating used cars dataset...")
    df = generate_used_cars_dataset(600)

    # Save to CSV
    output_file = 'used_cars_dataset.csv'
    df.to_csv(output_file, index=False)

    print(f"Dataset generated successfully!")
    print(f"Total records: {len(df)}")
    print(f"Saved to: {output_file}")
    print(f"\nDataset info:")
    print(f"Brands: {df['brand'].nunique()}")
    print(f"Models: {df['model'].nunique()}")
    print(f"Body types: {df['body_type'].unique()}")
    print(f"Registration years: {df['registration_year'].min()} - {df['registration_year'].max()}")
    print(f"Price range: Rs {df['current_price'].min():,.0f} - Rs {df['current_price'].max():,.0f}")
    print(f"\nFirst few records:")
    print(df.head())
