"""
Train ML model for used car price prediction
Target: 88%+ accuracy (R² score)
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import json
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

class UsedCarPricePredictor:
    """Class to train and evaluate used car price prediction models"""

    def __init__(self, data_path):
        """Initialize with dataset path"""
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}

    def load_and_prepare_data(self):
        """Load and prepare the dataset"""
        print("Loading dataset...")
        self.df = pd.read_csv(self.data_path)
        print(f"Dataset loaded: {len(self.df)} records")

        # Convert date column
        self.df['listing_date'] = pd.to_datetime(self.df['listing_date'])

        # Feature engineering
        # Calculate depreciation percentage
        self.df['depreciation'] = ((self.df['original_price'] - self.df['current_price']) /
                                  self.df['original_price'] * 100)

        # Price per km driven
        self.df['price_per_km'] = self.df['current_price'] / (self.df['mileage_km'] + 1)

        # Average km per year
        self.df['avg_km_per_year'] = self.df['mileage_km'] / (self.df['age_years'] + 1)

        print(f"\nDataset statistics:")
        print(self.df[['current_price', 'age_years', 'mileage_km', 'condition_score']].describe())

        return self.df

    def prepare_features(self):
        """Prepare features for training"""
        print("\nPreparing features...")

        # Select features for training
        feature_columns = [
            'brand', 'body_type', 'registration_year', 'age_years',
            'fuel_type', 'transmission', 'mileage_km', 'num_owners',
            'original_price', 'condition_score', 'insurance_validity_months',
            'service_history', 'accident_history', 'seating_capacity',
            'engine_cc', 'fuel_efficiency_kmpl', 'avg_km_per_year'
        ]

        X = self.df[feature_columns].copy()
        y = self.df['current_price']

        # Handle missing values
        print(f"Missing values before cleaning:")
        print(X.isnull().sum())

        # Fill missing values
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if X[col].isnull().any():
                X[col].fillna(X[col].median(), inplace=True)

        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if X[col].isnull().any():
                X[col].fillna(X[col].mode()[0], inplace=True)

        print(f"\nMissing values after cleaning:")
        print(X.isnull().sum())

        # Encode categorical variables
        categorical_columns = ['brand', 'body_type', 'fuel_type', 'transmission',
                              'service_history', 'accident_history']

        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le

        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

        print(f"Training set: {len(self.X_train)} samples")
        print(f"Test set: {len(self.X_test)} samples")
        print(f"Target (price) range: Rs {y.min():,.0f} - Rs {y.max():,.0f}")

        return self.X_train, self.X_test, self.y_train, self.y_test

    def train_random_forest(self):
        """Train Random Forest Regressor"""
        print("\n" + "="*50)
        print("Training Random Forest Regressor...")
        print("="*50)

        rf_model = RandomForestRegressor(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

        rf_model.fit(self.X_train_scaled, self.y_train)

        # Predictions
        y_pred = rf_model.predict(self.X_test_scaled)

        # Evaluation metrics
        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)
        mape = np.mean(np.abs((self.y_test - y_pred) / self.y_test)) * 100

        self.models['random_forest'] = rf_model
        self.results['random_forest'] = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2_score': r2,
            'mape': mape,
            'accuracy_percent': r2 * 100
        }

        print(f"Mean Absolute Error: Rs {mae:,.0f}")
        print(f"Root Mean Squared Error: Rs {rmse:,.0f}")
        print(f"R² Score: {r2:.4f} ({r2*100:.2f}%)")
        print(f"MAPE: {mape:.2f}%")

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.X_train.columns,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\nTop 10 Important Features:")
        print(feature_importance.head(10))

        return rf_model

    def train_gradient_boosting(self):
        """Train Gradient Boosting Regressor"""
        print("\n" + "="*50)
        print("Training Gradient Boosting Regressor...")
        print("="*50)

        gb_model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )

        gb_model.fit(self.X_train_scaled, self.y_train)

        # Predictions
        y_pred = gb_model.predict(self.X_test_scaled)

        # Evaluation metrics
        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)
        mape = np.mean(np.abs((self.y_test - y_pred) / self.y_test)) * 100

        self.models['gradient_boosting'] = gb_model
        self.results['gradient_boosting'] = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2_score': r2,
            'mape': mape,
            'accuracy_percent': r2 * 100
        }

        print(f"Mean Absolute Error: Rs {mae:,.0f}")
        print(f"Root Mean Squared Error: Rs {rmse:,.0f}")
        print(f"R² Score: {r2:.4f} ({r2*100:.2f}%)")
        print(f"MAPE: {mape:.2f}%")

        return gb_model

    def train_xgboost(self):
        """Train XGBoost Regressor"""
        print("\n" + "="*50)
        print("Training XGBoost Regressor...")
        print("="*50)

        xgb_model = XGBRegressor(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.1,
            min_child_weight=2,
            random_state=42,
            n_jobs=-1
        )

        xgb_model.fit(self.X_train_scaled, self.y_train)

        # Predictions
        y_pred = xgb_model.predict(self.X_test_scaled)

        # Evaluation metrics
        mae = mean_absolute_error(self.y_test, y_pred)
        mse = mean_squared_error(self.y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test, y_pred)
        mape = np.mean(np.abs((self.y_test - y_pred) / self.y_test)) * 100

        self.models['xgboost'] = xgb_model
        self.results['xgboost'] = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2_score': r2,
            'mape': mape,
            'accuracy_percent': r2 * 100
        }

        print(f"Mean Absolute Error: Rs {mae:,.0f}")
        print(f"Root Mean Squared Error: Rs {rmse:,.0f}")
        print(f"R² Score: {r2:.4f} ({r2*100:.2f}%)")
        print(f"MAPE: {mape:.2f}%")

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.X_train.columns,
            'importance': xgb_model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\nTop 10 Important Features:")
        print(feature_importance.head(10))

        return xgb_model

    def compare_models(self):
        """Compare all trained models"""
        print("\n" + "="*50)
        print("MODEL COMPARISON")
        print("="*50)

        comparison_df = pd.DataFrame(self.results).T
        comparison_df = comparison_df.sort_values('r2_score', ascending=False)

        print(comparison_df)

        # Find best model
        best_model_name = comparison_df.index[0]
        print(f"\nBest Model: {best_model_name.upper()}")
        print(f"R² Score: {comparison_df.loc[best_model_name, 'r2_score']:.4f} ({comparison_df.loc[best_model_name, 'accuracy_percent']:.2f}%)")
        print(f"RMSE: Rs {comparison_df.loc[best_model_name, 'rmse']:,.0f}")

        return comparison_df

    def create_visualizations(self, output_dir='trained_models'):
        """Create visualizations"""
        print("\nCreating visualizations...")

        # Use best model
        best_model_name = max(self.results.items(), key=lambda x: x[1]['r2_score'])[0]
        best_model = self.models[best_model_name]

        # Predictions
        y_pred = best_model.predict(self.X_test_scaled)

        # 1. Actual vs Predicted
        plt.figure(figsize=(10, 6))
        plt.scatter(self.y_test, y_pred, alpha=0.5)
        plt.plot([self.y_test.min(), self.y_test.max()],
                [self.y_test.min(), self.y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual Price (Rs)')
        plt.ylabel('Predicted Price (Rs)')
        plt.title(f'Actual vs Predicted Prices - {best_model_name.title()}')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'price_prediction_scatter.png'), dpi=100)
        plt.close()

        # 2. Residuals
        residuals = self.y_test - y_pred
        plt.figure(figsize=(10, 6))
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='--', lw=2)
        plt.xlabel('Predicted Price (Rs)')
        plt.ylabel('Residuals (Rs)')
        plt.title('Residual Plot')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'residuals_plot.png'), dpi=100)
        plt.close()

        print("Visualizations saved successfully!")

    def save_models(self, output_dir='trained_models'):
        """Save all trained models"""
        print(f"\nSaving models to {output_dir}/...")

        for model_name, model in self.models.items():
            model_path = os.path.join(output_dir, f'{model_name}_price_prediction.pkl')
            joblib.dump(model, model_path)
            print(f"Saved: {model_path}")

        # Save label encoders and scaler
        encoders_path = os.path.join(output_dir, 'price_label_encoders.pkl')
        joblib.dump(self.label_encoders, encoders_path)
        print(f"Saved: {encoders_path}")

        scaler_path = os.path.join(output_dir, 'price_scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        print(f"Saved: {scaler_path}")

        # Save results
        results_path = os.path.join(output_dir, 'price_prediction_results.json')
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"Saved: {results_path}")

        # Save feature names
        feature_names_path = os.path.join(output_dir, 'price_feature_names.pkl')
        joblib.dump(list(self.X_train.columns), feature_names_path)
        print(f"Saved: {feature_names_path}")

        print("\nAll models saved successfully!")

    def generate_report(self, output_dir='trained_models'):
        """Generate evaluation report"""
        report_path = os.path.join(output_dir, 'price_prediction_report.txt')

        with open(report_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("USED CAR PRICE PREDICTION MODEL - EVALUATION REPORT\n")
            f.write("="*70 + "\n\n")

            f.write(f"Dataset: {self.data_path}\n")
            f.write(f"Total Records: {len(self.df)}\n")
            f.write(f"Training Set: {len(self.X_train)} samples\n")
            f.write(f"Test Set: {len(self.X_test)} samples\n")
            f.write(f"Price Range: Rs {self.df['current_price'].min():,.0f} - Rs {self.df['current_price'].max():,.0f}\n\n")

            f.write("="*70 + "\n")
            f.write("MODEL PERFORMANCE COMPARISON\n")
            f.write("="*70 + "\n\n")

            for model_name, metrics in self.results.items():
                f.write(f"{model_name.upper()}\n")
                f.write("-" * 40 + "\n")
                f.write(f"R² Score:       {metrics['r2_score']:.4f} ({metrics['accuracy_percent']:.2f}%)\n")
                f.write(f"MAE:            Rs {metrics['mae']:,.0f}\n")
                f.write(f"RMSE:           Rs {metrics['rmse']:,.0f}\n")
                f.write(f"MAPE:           {metrics['mape']:.2f}%\n")
                f.write("\n")

            f.write("="*70 + "\n")
            f.write("TARGET ACHIEVEMENT\n")
            f.write("="*70 + "\n")

            best_model = max(self.results.items(), key=lambda x: x[1]['r2_score'])
            target_accuracy = 88.0

            f.write(f"Target Accuracy: {target_accuracy}%\n")
            f.write(f"Best Model: {best_model[0].upper()}\n")
            f.write(f"Achieved Accuracy: {best_model[1]['accuracy_percent']:.2f}%\n")

            if best_model[1]['accuracy_percent'] >= target_accuracy:
                f.write(f"\nSUCCESS! Target accuracy exceeded by {best_model[1]['accuracy_percent'] - target_accuracy:.2f}%\n")
            else:
                f.write(f"\nNeeds improvement: {target_accuracy - best_model[1]['accuracy_percent']:.2f}% below target\n")

            f.write("\n" + "="*70 + "\n")
            f.write("The model can accurately predict used car prices based on various features.\n")

        print(f"\nReport generated: {report_path}")


def main():
    """Main function to train all models"""
    # Path to dataset
    data_path = '../data/used_cars_dataset.csv'

    # Initialize predictor
    predictor = UsedCarPricePredictor(data_path)

    # Load and prepare data
    predictor.load_and_prepare_data()
    predictor.prepare_features()

    # Train all models
    predictor.train_random_forest()
    predictor.train_gradient_boosting()
    predictor.train_xgboost()

    # Compare models
    predictor.compare_models()

    # Create visualizations
    predictor.create_visualizations()

    # Save models
    predictor.save_models()

    # Generate report
    predictor.generate_report()

    print("\n" + "="*50)
    print("PRICE PREDICTION TRAINING COMPLETED!")
    print("="*50)


if __name__ == '__main__':
    main()
