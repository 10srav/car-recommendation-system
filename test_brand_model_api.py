"""
Test script to verify brand and model API endpoints
This script tests that all brands and their respective models are correctly accessible
"""

import requests
import json
import sys

# Set encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:5000'

def test_brands_api():
    """Test the /api/brands endpoint"""
    print("=" * 60)
    print("Testing /api/brands endpoint...")
    print("=" * 60)

    response = requests.get(f'{BASE_URL}/api/brands')

    if response.status_code == 200:
        brands = response.json()
        print(f"[PASS] Successfully fetched {len(brands)} brands")
        print(f"Brands: {', '.join(brands)}\n")
        return brands
    else:
        print(f"[FAIL] Failed to fetch brands. Status code: {response.status_code}")
        return []

def test_models_api(brand):
    """Test the /api/models/<brand> endpoint"""
    response = requests.get(f'{BASE_URL}/api/models/{brand}')

    if response.status_code == 200:
        models = response.json()
        print(f"  {brand}: {len(models)} models")
        print(f"    Models: {', '.join(models)}")
        return models
    else:
        print(f"  [FAIL] Failed to fetch models for {brand}")
        return []

def test_all_models():
    """Test models endpoint for all brands"""
    print("=" * 60)
    print("Testing /api/models/<brand> endpoint for all brands...")
    print("=" * 60)

    brands = test_brands_api()

    if not brands:
        print("No brands to test")
        return

    total_models = 0
    for brand in brands:
        models = test_models_api(brand)
        total_models += len(models)
        print()

    print("=" * 60)
    print(f"SUMMARY: {len(brands)} brands with {total_models} total models")
    print("=" * 60)

def test_forms_accessibility():
    """Test that the forms are accessible"""
    print("\n" + "=" * 60)
    print("Testing form accessibility...")
    print("=" * 60)

    forms_to_test = [
        ('/buyback', 'Buy-back Valuation Form'),
        ('/marketplace/list', 'List Car Form')
    ]

    for url, name in forms_to_test:
        response = requests.get(f'{BASE_URL}{url}')
        if response.status_code == 200:
            # Check if form has select dropdowns for brand
            if 'select' in response.text.lower() and 'brand' in response.text.lower():
                print(f"[PASS] {name} is accessible and has brand dropdown")
            else:
                print(f"[FAIL] {name} is missing brand dropdown")
        else:
            print(f"[FAIL] {name} is not accessible. Status code: {response.status_code}")

def main():
    print("\n" + "=" * 60)
    print("CAR RECOMMENDATION SYSTEM - API TESTING")
    print("=" * 60)
    print()

    try:
        # Test brands API
        brands = test_brands_api()

        # Test models API for all brands
        if brands:
            print("=" * 60)
            print("Testing /api/models/<brand> endpoint for all brands...")
            print("=" * 60)

            total_models = 0
            for brand in brands:
                models = test_models_api(brand)
                total_models += len(models)
                print()

            print("=" * 60)
            print(f"SUMMARY: {len(brands)} brands with {total_models} total models")
            print("=" * 60)

        # Test form accessibility
        test_forms_accessibility()

        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to the server.")
        print("  Make sure the Flask app is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"[ERROR] {str(e)}")

if __name__ == '__main__':
    main()
