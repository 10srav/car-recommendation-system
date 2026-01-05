# Car Recommendation System - Installation Guide

## Prerequisites

Before you begin, ensure you have the following installed on your computer:

### 1. Python 3.8 or Higher
- Download from: https://www.python.org/downloads/
- During installation, **check "Add Python to PATH"**
- Verify installation by opening Command Prompt and typing:
  ```
  python --version
  ```
  You should see something like: `Python 3.11.x`

### 2. Visual Studio Code
- Download from: https://code.visualstudio.com/
- Install with default settings

### 3. VS Code Python Extension
- Open VS Code
- Go to Extensions (Ctrl+Shift+X)
- Search for "Python" by Microsoft
- Click Install

---

## Installation Steps

### Step 1: Open Project in VS Code

1. Open VS Code
2. Go to **File > Open Folder**
3. Navigate to the `car-recommendation-system` folder
4. Click **Select Folder**

### Step 2: Open Terminal in VS Code

1. Go to **Terminal > New Terminal** (or press `Ctrl + ~`)
2. A terminal window will appear at the bottom

### Step 3: Create Virtual Environment (Recommended)

In the terminal, type:
```bash
python -m venv venv
```

Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### Step 4: Install Dependencies

Run the following command to install all required packages:
```bash
pip install -r requirements.txt
```

This will take 3-5 minutes depending on your internet speed.

### Step 5: Run the Application

Start the server:
```bash
python run.py
```

You will see:
```
============================================================
Indian Automotive Marketplace - Starting Server
============================================================

Access the application at: http://127.0.0.1:5000
```

### Step 6: Open in Browser

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **http://127.0.0.1:5000**
3. The application should load!

---

## Application Features

### Home Page
- Overview of the platform
- Statistics and featured cars

### Recommendations (/recommendations)
1. Click "Recommendations" in the navigation bar
2. Enter your budget (in INR)
3. Select preferences (fuel type, body type, etc.)
4. Click "Get Recommendations"
5. View personalized car suggestions

### Marketplace (/marketplace)
1. Click "Marketplace" in the navigation bar
2. Browse available used cars
3. Use filters to narrow down results
4. Click on any car to see full details

### Buy-Back Valuation (/buyback)
1. Click "Buy-Back" in the navigation bar
2. Enter your car details
3. Get instant valuation with price range

### EMI Calculator (/emi-calculator)
1. Click "EMI Calculator" in the navigation bar
2. Enter loan amount, interest rate, and tenure
3. Calculate monthly EMI payments

---

## Stopping the Server

To stop the application:
1. Go to the terminal in VS Code
2. Press `Ctrl + C`

---

## Troubleshooting

### Issue: "python is not recognized as an internal or external command"
**Solution:** Python is not in your PATH. Reinstall Python and check "Add Python to PATH".

### Issue: Port 5000 already in use
**Solution:**
1. Open `run.py` in VS Code
2. Change `port=5000` to `port=5001` on line 23
3. Save the file
4. Run again and access http://127.0.0.1:5001

### Issue: Module not found error
**Solution:** Make sure you activated the virtual environment, then run:
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Database error
**Solution:** Delete the database file and reload data:
```bash
del automotive_marketplace.db
python utils/load_data.py
```

### Issue: Application shows blank page
**Solution:**
1. Clear browser cache (Ctrl+Shift+Del)
2. Hard refresh the page (Ctrl+Shift+R)

---

## Project Structure

```
car-recommendation-system/
├── app/                    # Main application code
├── data/                   # Car datasets (CSV files)
├── models/                 # Machine learning models
│   └── trained_models/     # Pre-trained ML models
├── static/                 # CSS and JavaScript files
├── templates/              # HTML templates
├── utils/                  # Helper functions
├── config/                 # Configuration settings
├── requirements.txt        # Python dependencies
└── run.py                  # Main entry point
```

---

## Technical Specifications

- **Framework:** Flask 3.0
- **Database:** SQLite
- **ML Models:** XGBoost, Random Forest, Decision Tree
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Python Version:** 3.8+

---

## Support

For technical issues or questions, please contact the development team.

---

*Last Updated: December 2025*
