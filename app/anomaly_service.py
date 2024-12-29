import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
import joblib
import os
from typing import Dict, Tuple, List
import pandas as pd
import json

class AnomalyDetector:
    def __init__(self, model_path: str = "models/isolation_forest.joblib"):
        self.model_path = model_path
        self.model = None
        self.categories = {
            'food': 1,
            'transport': 2,
            'entertainment': 3,
            'bills': 4,
            'other': 0
        }
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or load the model"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print("Model loaded successfully")
            else:
                print("Training new model")
                self.model = IsolationForest(
                    contamination=0.1,
                    n_estimators=100,
                    max_samples='auto',
                    random_state=42
                )
                # Train with some default data
                default_data = [
                    {'amount': 100, 'category': 'food', 'date': '2024-01-01'},
                    {'amount': 200, 'category': 'transport', 'date': '2024-01-02'},
                    {'amount': 50, 'category': 'food', 'date': '2024-01-03'},
                    {'amount': 1000, 'category': 'bills', 'date': '2024-01-04'},
                    {'amount': 30, 'category': 'food', 'date': '2024-01-05'}
                ]
                features = np.array([self._preprocess_transaction(t) for t in default_data])
                self.model.fit(features)
                
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.model = None

    def analyze_transaction(self, transaction: Dict) -> Dict:
        """Analyze a transaction and provide detailed insights"""
        is_anomaly, confidence = self.detect_anomaly(transaction)
        
        category = transaction['category']
        amount = float(transaction['amount'])
        
        # Create analysis dict with proper string formatting
        insights = {
            'amount_analysis': self._analyze_amount(amount, category),
            'timing_analysis': self._analyze_timing(transaction['date']),
            'category_frequency': self._analyze_category(category)
        }
        
        # Ensure the entire response is JSON serializable
        analysis = {
            'is_anomaly': 1 if is_anomaly else 0,  # Use integers instead of booleans
            'confidence_score': float(confidence),
            'insights': insights
        }
        
        # Validate JSON serialization
        try:
            json.dumps(analysis)  # Test if the response can be serialized
            return analysis
        except Exception as e:
            print(f"JSON serialization error: {e}")
            # Return a sanitized version if there's an error
            return {
                'is_anomaly': 1 if is_anomaly else 0,
                'confidence_score': float(confidence),
                'insights': {
                    'amount_analysis': 'Amount analysis unavailable',
                    'timing_analysis': 'Timing analysis unavailable',
                    'category_frequency': 'Category analysis unavailable'
                }
            }

    def _analyze_amount(self, amount: float, category: str) -> str:
        """Analyze transaction amount"""
        if amount > 1000:
            return "High value transaction"
        elif amount < 10:
            return "Low value transaction"
        return "Normal transaction amount"
    
    def _analyze_timing(self, date_str: str) -> str:
        """Analyze transaction timing"""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if date.weekday() >= 5:
            return "Weekend transaction"
        return "Weekday transaction"
    
    def _analyze_category(self, category: str) -> str:
        """Analyze category with proper string formatting"""
        return f"Transaction category: {category}"

    def train(self, transactions: List[Dict]):
        """Train the model with historical transactions"""
        if not transactions:
            return False
        
        features = np.array([self._preprocess_transaction(t) for t in transactions])
        self.model.fit(features)
        
        # Save the model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        return True

    def _preprocess_transaction(self, transaction: Dict) -> List[float]:
        """Preprocess a single transaction into features"""
        amount = float(transaction['amount'])
        
        # Amount normalization (log scale to handle different ranges)
        normalized_amount = np.log1p(amount)
        
        # Category encoding
        category_code = self._encode_category(transaction['category'])
        
        # Time-based features
        date_features = self._extract_date_features(transaction['date'])
        
        # Combine all features
        features = [normalized_amount, category_code] + date_features
        
        return features
    
    def _encode_category(self, category: str) -> int:
        """Encode transaction category"""
        return self.categories.get(category.lower(), 0)
    
    def _extract_date_features(self, date_str: str) -> List[float]:
        """Extract multiple features from date"""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return [
            float(date.weekday()),  # Day of week (0-6)
            float(date.day),        # Day of month (1-31)
            float(date.month),      # Month (1-12)
        ]
    
    def detect_anomaly(self, transaction: Dict) -> Tuple[bool, float]:
        """Detect if a transaction is anomalous"""
        if self.model is None:
            raise ValueError("Model not initialized")
        
        features = self._preprocess_transaction(transaction)
        features = np.array(features).reshape(1, -1)
        
        prediction = self.model.predict(features)[0]
        score = self.model.score_samples(features)[0]
        
        is_anomaly = prediction == -1
        confidence = 1 - (score + abs(self.model.offset_)) / (2 * abs(self.model.offset_))
        
        return is_anomaly, float(confidence)

    def _preprocess_transaction(self, transaction: Dict) -> List[float]:
        """Preprocess a single transaction into features"""
        amount = float(transaction['amount'])
        normalized_amount = np.log1p(amount)
        category_code = self._encode_category(transaction['category'])
        date_features = self._extract_date_features(transaction['date'])
        return [normalized_amount, category_code] + date_features
    
    def _encode_category(self, category: str) -> int:
        """Encode transaction category"""
        return self.categories.get(category.lower(), 0)
    
    def _extract_date_features(self, date_str: str) -> List[float]:
        """Extract multiple features from date"""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return [
            float(date.weekday()),
            float(date.day),
            float(date.month)
        ]

def get_anomaly_detector():
    """Factory function to get anomaly detector instance"""
    return AnomalyDetector()