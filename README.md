# MyCar - Smart Car Marketplace

A modern web application for car recommendations, used car marketplace, and buy-back valuation powered by machine learning.

## Features

### Core Features
- **Smart Car Recommendations** - Get personalized car suggestions based on your budget, preferences, and lifestyle using AI/ML algorithms
- **Used Car Marketplace** - Browse and list used cars with AI-powered price predictions
- **Buy-Back Valuation** - Get instant, accurate valuation for your car
- **EMI Calculator** - Calculate monthly loan installments
- **New Car Details** - View comprehensive specifications for new cars

### Technical Highlights
- XGBoost-powered recommendation engine (94.6% accuracy)
- Price prediction model (98.2% R² score)
- Real-time car valuations
- Responsive Bootstrap 5 UI with custom teal/blue theme
- RESTful API endpoints
- User authentication system

## Screenshots

The application features:
- Professional teal color scheme (#1a5f7a)
- Custom SVG car logo
- Mobile-responsive design
- Interactive recommendation cards with match scores

## Technologies Used

| Category | Technologies |
|----------|-------------|
| Backend | Python 3.8+, Flask |
| ML/AI | scikit-learn, XGBoost, pandas, numpy |
| Database | SQLite with SQLAlchemy ORM |
| Frontend | Bootstrap 5, jQuery, Chart.js |
| Authentication | Flask-JWT-Extended, Flask-Bcrypt |

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Git installed

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd car-recommendation-system
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python run.py
```

### Step 5: Open in Browser
```
http://127.0.0.1:5000
```

### Application URLs

| Feature | URL |
|---------|-----|
| Home | http://127.0.0.1:5000 |
| Recommendations | http://127.0.0.1:5000/recommendations |
| Marketplace | http://127.0.0.1:5000/marketplace |
| Buy-Back Valuation | http://127.0.0.1:5000/buyback |
| EMI Calculator | http://127.0.0.1:5000/emi-calculator |
| Login | http://127.0.0.1:5000/auth/login-page |
| Register | http://127.0.0.1:5000/auth/register-page |

### Full Setup (if starting fresh)

```bash
# Generate datasets
cd data
python generate_new_cars_data.py
python generate_used_cars_data.py
cd ..

# Train ML models
cd models
python train_recommendation_model.py
python train_price_prediction_model.py
cd ..

# Load database
python utils/load_data.py

# Run application
python run.py
```

## Project Structure

```
mycar/
├── app/                    # Flask application
│   ├── __init__.py        # App factory
│   ├── routes.py          # Route definitions
│   ├── models.py          # Database models
│   ├── ml_manager.py      # ML model singleton
│   └── schemas.py         # Validation schemas
├── models/                 # ML model training
│   ├── trained_models/    # Saved model files
│   ├── train_recommendation_model.py
│   └── train_price_prediction_model.py
├── data/                   # Datasets (CSV)
├── templates/              # Jinja2 HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Homepage
│   ├── recommendations/   # Recommendation pages
│   ├── marketplace/       # Marketplace pages
│   └── buyback/           # Buy-back pages
├── static/                 # Static assets
│   ├── css/style.css      # Custom styles
│   └── js/main.js         # JavaScript
├── utils/                  # Helper functions
├── config/                 # Configuration
└── run.py                  # Entry point
```

## ML Models

### Recommendation Engine
| Algorithm | Accuracy |
|-----------|----------|
| Decision Tree | 89.2% |
| Random Forest | 92.1% |
| **XGBoost** | **94.6%** |

Features used: Budget, fuel type, body type, transmission, usage type, priority factor, family size

### Price Prediction
| Algorithm | R² Score |
|-----------|----------|
| Random Forest | 96.8% |
| Gradient Boosting | 97.5% |
| **XGBoost** | **98.2%** |

Features used: Age, mileage, condition, brand, service history, accident history

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/recommendations` | Get personalized car recommendations |
| POST | `/api/predict-price` | Predict used car price |
| POST | `/api/buyback-valuation` | Get buy-back valuation |
| GET | `/api/brands` | List all car brands |
| GET | `/api/models/<brand>` | Get models for a brand |
| GET | `/new-car/<id>` | View new car details |

## Database Schema

| Table | Description |
|-------|-------------|
| `new_cars` | New car inventory with specs |
| `used_cars` | Used car listings |
| `users` | User accounts |
| `valuations` | Buy-back valuation requests |
| `recommendation_history` | User recommendation logs |
| `transactions` | Transaction records |

## Usage Guide

### Get Recommendations
1. Navigate to **Recommendations** page
2. Set your budget range (min/max)
3. Select preferences (fuel, body type, transmission)
4. Choose priority (safety, mileage, performance, comfort)
5. Click "Get Recommendations"
6. View top 5 AI-matched cars with confidence scores
7. Click "View Full Details" for complete specifications

### Browse Marketplace
1. Go to **Marketplace** page
2. Apply filters (brand, price range, year, fuel type)
3. Browse available used cars
4. Click on any car for detailed view with price analysis

### Get Buy-Back Valuation
1. Visit **Buy-Back** page
2. Enter your car details (brand, model, year, mileage)
3. Provide condition information
4. Get instant AI-powered valuation with price range

## Troubleshooting

**Port already in use:**
```bash
# Edit run.py and change port
app.run(debug=True, port=5001)
```

**Database error:**
```bash
# Windows
del automotive_marketplace_v2.db
python run.py

# Linux/Mac
rm automotive_marketplace_v2.db
python run.py
```

**Module not found:**
```bash
pip install --upgrade -r requirements.txt
```

**Virtual environment issues:**
```bash
# Deactivate and recreate
deactivate
rm -rf venv
python -m venv venv
# Then activate and install again
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes.

## Contact

For issues or questions, please create an issue in the repository.

---

**MyCar** - Your Smart Car Companion
