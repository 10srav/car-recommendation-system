"""
Script to load CSV data into the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, NewCar, UsedCar
import pandas as pd
from datetime import datetime

def load_new_cars(csv_path):
    """Load new cars data from CSV"""
    print("Loading new cars data...")
    df = pd.read_csv(csv_path)

    count = 0
    for _, row in df.iterrows():
        car = NewCar(
            car_id=int(row['car_id']),
            brand=row['brand'],
            model=row['model'],
            variant=row['variant'],
            body_type=row['body_type'],
            year=int(row['year']),
            price=int(row['price']),
            fuel_type=row['fuel_type'],
            mileage=float(row['mileage']),
            transmission=row['transmission'],
            seating_capacity=int(row['seating_capacity']),
            engine_cc=int(row['engine_cc']),
            power_hp=int(row['power_hp']),
            torque_nm=int(row['torque_nm']),
            safety_rating=int(row['safety_rating']),
            safety_features=row['safety_features'],
            comfort_features=row['comfort_features'],
            ground_clearance_mm=int(row['ground_clearance_mm']),
            boot_space_liters=int(row['boot_space_liters']),
            maintenance_cost_annual=int(row['maintenance_cost_annual']),
            warranty_years=int(row['warranty_years']),
            colors_available=int(row['colors_available']),
            resale_value_3yr_percent=float(row['resale_value_3yr_percent']),
            resale_value_5yr_percent=float(row['resale_value_5yr_percent']),
            city_suitability_score=float(row['city_suitability_score']),
            highway_suitability_score=float(row['highway_suitability_score']),
            mileage_score=float(row['mileage_score']),
            performance_score=float(row['performance_score']),
            safety_score=float(row['safety_score']),
            comfort_score=float(row['comfort_score'])
        )

        db.session.add(car)
        count += 1

        if count % 100 == 0:
            db.session.commit()
            print(f"Loaded {count} new cars...")

    db.session.commit()
    print(f"Total new cars loaded: {count}")


def load_used_cars(csv_path):
    """Load used cars data from CSV"""
    print("\nLoading used cars data...")
    df = pd.read_csv(csv_path)

    count = 0
    for _, row in df.iterrows():
        car = UsedCar(
            listing_id=int(row['listing_id']),
            brand=row['brand'],
            model=row['model'],
            variant=row['variant'],
            body_type=row['body_type'],
            registration_year=int(row['registration_year']),
            age_years=int(row['age_years']),
            fuel_type=row['fuel_type'],
            transmission=row['transmission'],
            mileage_km=int(row['mileage_km']),
            num_owners=int(row['num_owners']),
            original_price=int(row['original_price']),
            current_price=int(row['current_price']),
            condition_score=float(row['condition_score']),
            insurance_validity_months=int(row['insurance_validity_months']),
            service_history=row['service_history'],
            accident_history=row['accident_history'],
            color=row['color'],
            seating_capacity=int(row['seating_capacity']),
            engine_cc=int(row['engine_cc']),
            fuel_efficiency_kmpl=float(row['fuel_efficiency_kmpl']),
            rto=row['rto'],
            city=row['city'],
            features=row['features'],
            seller_name=row['seller_name'],
            seller_phone=row['seller_phone'],
            listing_date=pd.to_datetime(row['listing_date']).date(),
            negotiable=row['negotiable'],
            test_drive_available=row['test_drive_available'],
            is_sold=False
        )

        db.session.add(car)
        count += 1

        if count % 100 == 0:
            db.session.commit()
            print(f"Loaded {count} used cars...")

    db.session.commit()
    print(f"Total used cars loaded: {count}")


def main():
    """Main function"""
    app = create_app()

    with app.app_context():
        # Drop and recreate tables
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        print("Tables created successfully!")

        # Load data
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        new_cars_csv = os.path.join(base_dir, 'data', 'new_cars_dataset.csv')
        used_cars_csv = os.path.join(base_dir, 'data', 'used_cars_dataset.csv')

        load_new_cars(new_cars_csv)
        load_used_cars(used_cars_csv)

        print("\n" + "="*50)
        print("Data loading completed successfully!")
        print("="*50)


if __name__ == '__main__':
    main()
