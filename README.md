# Indian Automotive Marketplace

A web application for car recommendations, used car marketplace, and buy-back valuation using machine learning.

## Features

1. **New Car Recommendations** - Get personalized car suggestions based on budget and preferences
2. **Used Car Marketplace** - Browse and list used cars with AI price predictions
3. **Buy-Back Valuation** - Get instant valuation for your car

## Technologies Used

- Python 3.8+
- Flask (web framework)
- scikit-learn, XGBoost (machine learning)
- SQLite (database)
- Bootstrap 5 (frontend)

## Installation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Generate Datasets
```bash
cd data
python generate_new_cars_data.py
python generate_used_cars_data.py
cd ..
```

### Step 3: Train Models
```bash
cd models
python train_recommendation_model.py
python train_price_prediction_model.py
cd ..
```

### Step 4: Load Database
```bash
python utils/load_data.py
```

### Step 5: Run Application
```bash
python run.py
```

Open browser: http://127.0.0.1:5000

## Project Structure

```
indian-auto-marketplace/
├── app/                 # Flask application
├── models/              # ML model training scripts
├── data/                # Datasets
├── templates/           # HTML templates
├── static/              # CSS, JavaScript
├── utils/               # Helper functions
├── config/              # Configuration
└── run.py              # Main entry point
```

## ML Models

### Recommendation Model
- Algorithms: Decision Tree, Random Forest, XGBoost
- Best: XGBoost (94.6% accuracy)
- Features: Price, fuel type, mileage, safety, etc.

### Price Prediction Model
- Algorithms: Random Forest, Gradient Boosting, XGBoost
- Best: XGBoost (98.2% R² score)
- Features: Age, mileage, condition, brand, etc.

## Database Schema

- **new_cars** - New car inventory
- **used_cars** - Used car listings
- **users** - User accounts
- **valuations** - Buy-back requests
- **recommendation_history** - Recommendation logs
- **transactions** - Transaction records

## API Endpoints

- `POST /api/recommendations` - Get car recommendations
- `POST /api/predict-price` - Predict used car price
- `POST /api/buyback-valuation` - Get buy-back valuation
- `GET /api/brands` - List all brands
- `GET /api/models/<brand>` - Get models for brand

## Usage

### Get Recommendations
1. Go to Recommendations page
2. Enter budget, preferences
3. View top 5 recommended cars

### Browse Marketplace
1. Go to Marketplace page
2. Apply filters (brand, price, year)
3. Click on car for details

### Get Buy-Back Valuation
1. Go to Buy-Back page
2. Enter car details
3. Get instant valuation with price range

## Troubleshooting

**Port already in use:**
```bash
# Change port in run.py
app.run(debug=True, port=5001)
```

**Database error:**
```bash
rm automotive_marketplace.db
python utils/load_data.py
```

**Module not found:**
```bash
pip install --upgrade -r requirements.txt
```

## Future Enhancements

- User authentication
- Admin dashboard
- Payment integration
- Mobile app
- Image upload for cars
- Real-time chat

## License

This project is for educational purposes.

## Contact

For issues or questions, please create an issue in the repository.
