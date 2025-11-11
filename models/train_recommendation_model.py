# Car Recommendation ML Model Training
# This file trains multiple models and picks the best one
# TODO: maybe try neural networks later if we have time

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
import os
import json

class CarRecommendationModel:
    # Main class for training recommendation models

    def __init__(self, data_path):
        # Initialize everything
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

        # Create a target variable for recommendation
        # We'll create user preferences and match cars to them
        # For training, we'll create synthetic preference-based labels

        # Feature engineering
        self.df['price_category'] = pd.cut(self.df['price'],
                                           bins=[0, 500000, 1000000, 1500000, 2000000, float('inf')],
                                           labels=['Budget', 'Mid-Range', 'Premium', 'Luxury', 'Super-Luxury'])

        self.df['mileage_category'] = pd.cut(self.df['mileage'],
                                             bins=[0, 15, 20, 25, float('inf')],
                                             labels=['Low', 'Medium', 'High', 'Very-High'])

        # Create composite suitability score for classification
        self.df['overall_score'] = (
            self.df['mileage_score'] * 0.25 +
            self.df['performance_score'] * 0.20 +
            self.df['safety_score'] * 0.30 +
            self.df['comfort_score'] * 0.25
        )

        # Create recommendation categories based on overall score
        # Using 3 classes to avoid class imbalance issues
        self.df['recommendation_class'] = pd.cut(self.df['overall_score'],
                                                 bins=[0, 6, 8, 10],
                                                 labels=['Fair', 'Good', 'Excellent'])

        print(f"Recommendation class distribution:")
        print(self.df['recommendation_class'].value_counts())

        return self.df

    def prepare_features(self):
        """Prepare features for training"""
        print("\nPreparing features...")

        # Select features for training
        feature_columns = [
            'price', 'fuel_type', 'transmission', 'body_type',
            'seating_capacity', 'mileage', 'power_hp', 'safety_rating',
            'warranty_years', 'maintenance_cost_annual',
            'city_suitability_score', 'highway_suitability_score'
        ]

        X = self.df[feature_columns].copy()
        y = self.df['recommendation_class']

        # Handle missing values
        print(f"Missing values before cleaning:")
        print(X.isnull().sum())

        # Fill missing values with median for numeric columns
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if X[col].isnull().any():
                X[col].fillna(X[col].median(), inplace=True)

        # Remove rows with missing target values
        mask = ~y.isnull()
        X = X[mask]
        y = y[mask]

        print(f"\nMissing values after cleaning:")
        print(X.isnull().sum())

        # Encode categorical variables
        categorical_columns = ['fuel_type', 'transmission', 'body_type']

        for col in categorical_columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.label_encoders[col] = le

        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

        print(f"Training set: {len(self.X_train)} samples")
        print(f"Test set: {len(self.X_test)} samples")

        return self.X_train, self.X_test, self.y_train, self.y_test

    def train_decision_tree(self):
        """Train Decision Tree model"""
        print("\n" + "="*50)
        print("Training Decision Tree Model...")
        print("="*50)

        dt_model = DecisionTreeClassifier(
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10,
            random_state=42
        )

        dt_model.fit(self.X_train_scaled, self.y_train)

        # Predictions
        y_pred = dt_model.predict(self.X_test_scaled)

        # Evaluation
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(self.y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(self.y_test, y_pred, average='weighted', zero_division=0)

        # Cross-validation
        cv_scores = cross_val_score(dt_model, self.X_train_scaled, self.y_train, cv=5)

        self.models['decision_tree'] = dt_model
        self.results['decision_tree'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }

        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print(f"Cross-Validation Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

        return dt_model

    def train_random_forest(self):
        """Train Random Forest model"""
        print("\n" + "="*50)
        print("Training Random Forest Model...")
        print("="*50)

        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1
        )

        rf_model.fit(self.X_train_scaled, self.y_train)

        # Predictions
        y_pred = rf_model.predict(self.X_test_scaled)

        # Evaluation
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(self.y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(self.y_test, y_pred, average='weighted', zero_division=0)

        # Cross-validation
        cv_scores = cross_val_score(rf_model, self.X_train_scaled, self.y_train, cv=5)

        self.models['random_forest'] = rf_model
        self.results['random_forest'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }

        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print(f"Cross-Validation Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.X_train.columns,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\nTop 5 Important Features:")
        print(feature_importance.head())

        return rf_model

    def train_xgboost(self):
        """Train XGBoost model"""
        print("\n" + "="*50)
        print("Training XGBoost Model...")
        print("="*50)

        # Encode target labels for XGBoost
        le_target = LabelEncoder()
        y_train_encoded = le_target.fit_transform(self.y_train)
        y_test_encoded = le_target.transform(self.y_test)

        xgb_model = XGBClassifier(
            n_estimators=100,
            max_depth=8,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1,
            eval_metric='mlogloss'
        )

        xgb_model.fit(self.X_train_scaled, y_train_encoded)

        # Predictions
        y_pred_encoded = xgb_model.predict(self.X_test_scaled)
        y_pred = le_target.inverse_transform(y_pred_encoded)

        # Evaluation
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(self.y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(self.y_test, y_pred, average='weighted', zero_division=0)

        # Cross-validation
        cv_scores = cross_val_score(xgb_model, self.X_train_scaled, y_train_encoded, cv=5)

        self.models['xgboost'] = xgb_model
        self.label_encoders['target'] = le_target
        self.results['xgboost'] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }

        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
        print(f"Cross-Validation Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.X_train.columns,
            'importance': xgb_model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\nTop 5 Important Features:")
        print(feature_importance.head())

        return xgb_model

    def compare_models(self):
        """Compare all trained models"""
        print("\n" + "="*50)
        print("MODEL COMPARISON")
        print("="*50)

        comparison_df = pd.DataFrame(self.results).T
        comparison_df = comparison_df.sort_values('accuracy', ascending=False)

        print(comparison_df)

        # Find best model
        best_model_name = comparison_df.index[0]
        print(f"\nBest Model: {best_model_name.upper()}")
        print(f"Accuracy: {comparison_df.loc[best_model_name, 'accuracy']:.4f}")

        return comparison_df

    def save_models(self, output_dir='trained_models'):
        """Save all trained models"""
        os.makedirs(output_dir, exist_ok=True)

        print(f"\nSaving models to {output_dir}/...")

        for model_name, model in self.models.items():
            model_path = os.path.join(output_dir, f'{model_name}_recommendation.pkl')
            joblib.dump(model, model_path)
            print(f"Saved: {model_path}")

        # Save label encoders and scaler
        encoders_path = os.path.join(output_dir, 'label_encoders.pkl')
        joblib.dump(self.label_encoders, encoders_path)
        print(f"Saved: {encoders_path}")

        scaler_path = os.path.join(output_dir, 'scaler.pkl')
        joblib.dump(self.scaler, scaler_path)
        print(f"Saved: {scaler_path}")

        # Save results
        results_path = os.path.join(output_dir, 'model_comparison_results.json')
        with open(results_path, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"Saved: {results_path}")

        print("\nAll models saved successfully!")

    def generate_report(self, output_dir='trained_models'):
        """Generate evaluation report"""
        report_path = os.path.join(output_dir, 'recommendation_model_report.txt')

        with open(report_path, 'w') as f:
            f.write("="*70 + "\n")
            f.write("NEW CAR RECOMMENDATION MODEL - EVALUATION REPORT\n")
            f.write("="*70 + "\n\n")

            f.write(f"Dataset: {self.data_path}\n")
            f.write(f"Total Records: {len(self.df)}\n")
            f.write(f"Training Set: {len(self.X_train)} samples\n")
            f.write(f"Test Set: {len(self.X_test)} samples\n\n")

            f.write("="*70 + "\n")
            f.write("MODEL PERFORMANCE COMPARISON\n")
            f.write("="*70 + "\n\n")

            for model_name, metrics in self.results.items():
                f.write(f"{model_name.upper()}\n")
                f.write("-" * 40 + "\n")
                f.write(f"Accuracy:       {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)\n")
                f.write(f"Precision:      {metrics['precision']:.4f}\n")
                f.write(f"Recall:         {metrics['recall']:.4f}\n")
                f.write(f"F1 Score:       {metrics['f1_score']:.4f}\n")
                f.write(f"CV Score:       {metrics['cv_mean']:.4f} (+/- {metrics['cv_std']:.4f})\n")
                f.write("\n")

            f.write("="*70 + "\n")
            f.write("RECOMMENDATION\n")
            f.write("="*70 + "\n")

            best_model = max(self.results.items(), key=lambda x: x[1]['accuracy'])
            f.write(f"Best performing model: {best_model[0].upper()}\n")
            f.write(f"Accuracy: {best_model[1]['accuracy']:.4f} ({best_model[1]['accuracy']*100:.2f}%)\n\n")

            f.write("All models have been trained and saved successfully.\n")
            f.write("The models can be used for real-time car recommendations.\n")

        print(f"\nReport generated: {report_path}")


def main():
    """Main function to train all models"""
    # Path to dataset
    data_path = '../data/new_cars_dataset.csv'

    # Initialize model trainer
    trainer = CarRecommendationModel(data_path)

    # Load and prepare data
    trainer.load_and_prepare_data()
    trainer.prepare_features()

    # Train all models
    trainer.train_decision_tree()
    trainer.train_random_forest()
    trainer.train_xgboost()

    # Compare models
    trainer.compare_models()

    # Save models
    trainer.save_models()

    # Generate report
    trainer.generate_report()

    print("\n" + "="*50)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*50)


if __name__ == '__main__':
    main()
