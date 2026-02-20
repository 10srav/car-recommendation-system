# Main file to run the Flask app
# Run this file: python run.py

import os
from app import create_app
from app.models import db, NewCar, UsedCar

app = create_app('development')


def seed_database():
    """Auto-seed database from CSV files if tables are empty."""
    new_count = NewCar.query.count()
    used_count = UsedCar.query.count()

    if new_count > 0 or used_count > 0:
        print(f"Database already has data ({new_count} new cars, {used_count} used cars). Skipping seed.")
        return

    print("Empty database detected — seeding from CSV files...")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    new_csv = os.path.join(base_dir, 'data', 'new_cars_dataset.csv')
    used_csv = os.path.join(base_dir, 'data', 'used_cars_dataset.csv')

    if not os.path.exists(new_csv) or not os.path.exists(used_csv):
        print("WARNING: CSV data files not found in data/ folder. Run generate scripts first.")
        return

    import pandas as pd
    from datetime import datetime

    # Load new cars
    df = pd.read_csv(new_csv)
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
    db.session.commit()
    print(f"  Loaded {len(df)} new cars.")

    # Load used cars
    df = pd.read_csv(used_csv)
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
    db.session.commit()
    print(f"  Loaded {len(df)} used cars.")
    print("Database seeded successfully!")


if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        seed_database()

    print("\n" + "="*60)
    print("MyCar - Starting Server")
    print("="*60)
    print("\nAccess the application at: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server\n")

    # Start the Flask development server
    # For production, use a proper WSGI server like gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
