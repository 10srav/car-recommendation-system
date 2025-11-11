"""
Script to generate synthetic new cars dataset for Indian automotive marketplace
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define Indian car brands and their models by segment
CAR_DATA = {
    'Maruti Suzuki': {
        'hatchback': ['Alto', 'Swift', 'Baleno', 'Celerio', 'Ignis', 'WagonR'],
        'sedan': ['Dzire', 'Ciaz'],
        'suv': ['Brezza', 'Grand Vitara', 'Ertiga', 'XL6'],
        'mpv': ['Ertiga', 'XL6']
    },
    'Hyundai': {
        'hatchback': ['i10', 'i20', 'Grand i10 Nios'],
        'sedan': ['Aura', 'Verna'],
        'suv': ['Venue', 'Creta', 'Alcazar', 'Tucson', 'Kona Electric'],
        'mpv': []
    },
    'Tata': {
        'hatchback': ['Tiago', 'Altroz'],
        'sedan': ['Tigor'],
        'suv': ['Punch', 'Nexon', 'Harrier', 'Safari', 'Nexon EV'],
        'mpv': []
    },
    'Mahindra': {
        'hatchback': [],
        'sedan': [],
        'suv': ['XUV300', 'XUV700', 'Scorpio', 'Scorpio N', 'Thar', 'Bolero', 'XUV400'],
        'mpv': ['Marazzo']
    },
    'Honda': {
        'hatchback': ['Jazz'],
        'sedan': ['Amaze', 'City'],
        'suv': ['Elevate'],
        'mpv': []
    },
    'Toyota': {
        'hatchback': ['Glanza'],
        'sedan': [],
        'suv': ['Urban Cruiser', 'Fortuner', 'Hilux', 'Land Cruiser'],
        'mpv': ['Innova Crysta', 'Innova Hycross']
    },
    'Kia': {
        'hatchback': [],
        'sedan': [],
        'suv': ['Sonet', 'Seltos', 'Carens', 'EV6'],
        'mpv': ['Carens']
    },
    'MG': {
        'hatchback': ['Comet EV'],
        'sedan': [],
        'suv': ['Astor', 'Hector', 'ZS EV'],
        'mpv': ['Hector Plus']
    },
    'Renault': {
        'hatchback': ['Kwid'],
        'sedan': [],
        'suv': ['Kiger', 'Duster'],
        'mpv': ['Triber']
    },
    'Nissan': {
        'hatchback': ['Magnite'],
        'sedan': [],
        'suv': ['Magnite'],
        'mpv': []
    }
}

# Fuel types and their typical mileage ranges
FUEL_MILEAGE = {
    'Petrol': (12, 24),
    'Diesel': (16, 28),
    'CNG': (20, 32),
    'Electric': (300, 500),  # km per charge
    'Hybrid': (20, 30)
}

# Transmission types
TRANSMISSIONS = ['Manual', 'Automatic', 'AMT', 'CVT', 'DCT']

# Safety features
SAFETY_FEATURES = [
    ['Dual Airbags', 'ABS', 'EBD'],
    ['Dual Airbags', 'ABS', 'EBD', 'Rear Parking Sensors'],
    ['6 Airbags', 'ABS', 'EBD', 'ESP', 'Rear Parking Sensors', 'Hill Hold Control'],
    ['6 Airbags', 'ABS', 'EBD', 'ESP', '360 Camera', 'Hill Hold Control', 'TPMS'],
    ['6 Airbags', 'ABS', 'EBD', 'ESP', '360 Camera', 'ADAS', 'Hill Hold Control', 'TPMS', 'Electronic Stability Control']
]

# Comfort features
COMFORT_FEATURES = [
    ['Power Windows', 'Central Locking'],
    ['Power Windows', 'Central Locking', 'AC', 'Power Steering'],
    ['Power Windows', 'Central Locking', 'Climate Control', 'Power Steering', 'Touchscreen Infotainment'],
    ['Automatic Climate Control', 'Touchscreen Infotainment', 'Wireless Charging', 'Cruise Control', 'Sunroof'],
    ['Dual Zone Climate Control', '10-inch Touchscreen', 'Wireless Charging', 'Ventilated Seats', 'Panoramic Sunroof', 'Premium Sound System']
]

def generate_new_cars_dataset(num_records=1200):
    """Generate synthetic new cars dataset"""

    data = []
    car_id = 1

    for _ in range(num_records):
        # Select random brand and body type
        brand = random.choice(list(CAR_DATA.keys()))
        body_type = random.choice(list(CAR_DATA[brand].keys()))

        # Skip if no models available for this combination
        if not CAR_DATA[brand][body_type]:
            continue

        model = random.choice(CAR_DATA[brand][body_type])

        # Generate variant name
        variants = ['Base', 'Mid', 'Top', 'LX', 'VX', 'ZX', 'EX', 'SX', 'Alpha']
        variant = random.choice(variants)

        # Determine fuel type based on model
        if 'EV' in model or 'Electric' in model or 'Kona' in model or 'ZS' in model:
            fuel_type = 'Electric'
        elif 'Hycross' in model:
            fuel_type = 'Hybrid'
        elif body_type == 'suv' and random.random() > 0.7:
            fuel_type = 'Diesel'
        elif random.random() > 0.8:
            fuel_type = random.choice(['CNG', 'Diesel'])
        else:
            fuel_type = 'Petrol'

        # Generate mileage based on fuel type
        mileage_range = FUEL_MILEAGE[fuel_type]
        mileage = round(random.uniform(mileage_range[0], mileage_range[1]), 1)

        # Generate price based on body type and features
        if body_type == 'hatchback':
            base_price = random.randint(400000, 1000000)  # 4L - 10L
        elif body_type == 'sedan':
            base_price = random.randint(600000, 1800000)  # 6L - 18L
        elif body_type == 'suv':
            base_price = random.randint(700000, 5000000)  # 7L - 50L
        else:  # mpv
            base_price = random.randint(800000, 3000000)  # 8L - 30L

        # Adjust price for variant and features
        variant_multiplier = {'Base': 1.0, 'Mid': 1.15, 'Top': 1.3, 'LX': 1.1,
                            'VX': 1.2, 'ZX': 1.3, 'EX': 1.25, 'SX': 1.2, 'Alpha': 1.35}
        price = int(base_price * variant_multiplier.get(variant, 1.0))

        # Electric cars premium
        if fuel_type == 'Electric':
            price = int(price * 1.4)

        # Generate seating capacity
        if body_type == 'hatchback':
            seating = random.choice([5, 5, 5, 5, 7])
        elif body_type == 'sedan':
            seating = 5
        elif body_type == 'suv':
            seating = random.choice([5, 5, 5, 7, 7])
        else:  # mpv
            seating = random.choice([7, 8])

        # Transmission
        if fuel_type == 'Electric':
            transmission = 'Automatic'
        elif variant in ['Top', 'Alpha', 'ZX']:
            transmission = random.choice(['Automatic', 'CVT', 'DCT', 'Manual'])
        else:
            transmission = random.choice(['Manual', 'Manual', 'Manual', 'AMT', 'Automatic'])

        # Engine capacity (CC)
        if fuel_type == 'Electric':
            engine_cc = 0
            power_hp = random.randint(80, 250)
        else:
            if body_type == 'hatchback':
                engine_cc = random.choice([800, 1000, 1200])
                power_hp = random.randint(60, 100)
            elif body_type == 'sedan':
                engine_cc = random.choice([1200, 1500, 1600])
                power_hp = random.randint(80, 120)
            else:  # suv/mpv
                engine_cc = random.choice([1500, 1600, 2000, 2200, 2500])
                power_hp = random.randint(100, 200)

        # Torque
        torque_nm = int(power_hp * random.uniform(1.2, 1.5))

        # Safety rating (1-5 stars)
        safety_rating = random.choices([3, 4, 5], weights=[0.2, 0.5, 0.3])[0]

        # Safety features based on price
        if price < 600000:
            safety_features = SAFETY_FEATURES[0]
        elif price < 1000000:
            safety_features = random.choice(SAFETY_FEATURES[1:3])
        elif price < 2000000:
            safety_features = random.choice(SAFETY_FEATURES[2:4])
        else:
            safety_features = SAFETY_FEATURES[4]

        # Comfort features based on price
        if price < 600000:
            comfort_features = COMFORT_FEATURES[0]
        elif price < 1000000:
            comfort_features = random.choice(COMFORT_FEATURES[1:3])
        elif price < 2000000:
            comfort_features = random.choice(COMFORT_FEATURES[2:4])
        else:
            comfort_features = COMFORT_FEATURES[4]

        # Ground clearance
        if body_type == 'suv':
            ground_clearance = random.randint(180, 220)
        elif body_type == 'hatchback':
            ground_clearance = random.randint(160, 180)
        else:
            ground_clearance = random.randint(165, 190)

        # Boot space
        if body_type == 'hatchback':
            boot_space = random.randint(250, 400)
        elif body_type == 'sedan':
            boot_space = random.randint(400, 550)
        else:
            boot_space = random.randint(200, 400)

        # Maintenance cost (annual in INR)
        maintenance_cost = int(price * random.uniform(0.02, 0.04))

        # Warranty (years)
        warranty_years = random.choice([3, 4, 5])

        # Launch year
        year = random.choice([2020, 2021, 2022, 2023, 2024, 2025])

        # Colors available
        colors_count = random.randint(5, 10)

        # Predicted resale value (percentage after years)
        resale_3_years = round(random.uniform(55, 70), 1)
        resale_5_years = round(random.uniform(40, 55), 1)

        # Usage type suitability scores (0-10)
        if body_type == 'hatchback':
            city_score = random.uniform(8, 10)
            highway_score = random.uniform(6, 8)
        elif body_type == 'sedan':
            city_score = random.uniform(7, 9)
            highway_score = random.uniform(7, 9)
        else:  # suv/mpv
            city_score = random.uniform(6, 8)
            highway_score = random.uniform(8, 10)

        # Features scores
        mileage_score = min(10, (mileage / 30) * 10)
        performance_score = min(10, (power_hp / 200) * 10)
        safety_score = safety_rating * 2
        comfort_score = len(comfort_features) / 5 * 10

        # Create record
        record = {
            'car_id': car_id,
            'brand': brand,
            'model': model,
            'variant': variant,
            'body_type': body_type,
            'year': year,
            'price': price,
            'fuel_type': fuel_type,
            'mileage': mileage,
            'transmission': transmission,
            'seating_capacity': seating,
            'engine_cc': engine_cc,
            'power_hp': power_hp,
            'torque_nm': torque_nm,
            'safety_rating': safety_rating,
            'safety_features': ', '.join(safety_features),
            'comfort_features': ', '.join(comfort_features),
            'ground_clearance_mm': ground_clearance,
            'boot_space_liters': boot_space,
            'maintenance_cost_annual': maintenance_cost,
            'warranty_years': warranty_years,
            'colors_available': colors_count,
            'resale_value_3yr_percent': resale_3_years,
            'resale_value_5yr_percent': resale_5_years,
            'city_suitability_score': round(city_score, 1),
            'highway_suitability_score': round(highway_score, 1),
            'mileage_score': round(mileage_score, 1),
            'performance_score': round(performance_score, 1),
            'safety_score': round(safety_score, 1),
            'comfort_score': round(comfort_score, 1)
        }

        data.append(record)
        car_id += 1

    # Create DataFrame
    df = pd.DataFrame(data)

    return df

if __name__ == '__main__':
    print("Generating new cars dataset...")
    df = generate_new_cars_dataset(1200)

    # Save to CSV
    output_file = 'new_cars_dataset.csv'
    df.to_csv(output_file, index=False)

    print(f"Dataset generated successfully!")
    print(f"Total records: {len(df)}")
    print(f"Saved to: {output_file}")
    print(f"\nDataset info:")
    print(f"Brands: {df['brand'].nunique()}")
    print(f"Models: {df['model'].nunique()}")
    print(f"Body types: {df['body_type'].unique()}")
    print(f"Price range: ₹{df['price'].min():,.0f} - ₹{df['price'].max():,.0f}")
    print(f"\nFirst few records:")
    print(df.head())
