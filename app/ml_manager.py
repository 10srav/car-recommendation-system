"""
ML Model Manager - Singleton pattern for efficient model loading
Models are loaded once at application startup, not on every request
"""
import threading
from utils.ml_helper import RecommendationEngine, PricePredictor, BuyBackValuator


class MLModelManager:
    """Singleton manager for ML models - ensures models are loaded only once"""

    _instance = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if MLModelManager._initialized:
            return

        with MLModelManager._lock:
            if MLModelManager._initialized:
                return

            self._recommendation_engine = None
            self._price_predictor = None
            self._buyback_valuator = None
            self._models_loaded = False
            MLModelManager._initialized = True

    def load_models(self):
        """Load all ML models - call this during app initialization"""
        if self._models_loaded:
            return

        with MLModelManager._lock:
            if self._models_loaded:
                return

            try:
                print("Loading ML models...")
                self._recommendation_engine = RecommendationEngine()
                self._price_predictor = PricePredictor()
                self._buyback_valuator = BuyBackValuator()
                self._models_loaded = True
                print("All ML models loaded successfully!")
            except Exception as e:
                print(f"Error loading ML models: {e}")
                raise

    @property
    def recommendation_engine(self):
        """Get recommendation engine (lazy load if not initialized)"""
        if not self._models_loaded:
            self.load_models()
        return self._recommendation_engine

    @property
    def price_predictor(self):
        """Get price predictor (lazy load if not initialized)"""
        if not self._models_loaded:
            self.load_models()
        return self._price_predictor

    @property
    def buyback_valuator(self):
        """Get buyback valuator (lazy load if not initialized)"""
        if not self._models_loaded:
            self.load_models()
        return self._buyback_valuator

    @property
    def is_loaded(self):
        """Check if models are loaded"""
        return self._models_loaded


# Global instance - use this throughout the application
ml_models = MLModelManager()
