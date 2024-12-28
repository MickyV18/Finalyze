import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.1,  # Adjust based on your needs
            random_state=42
        )
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        try:
            # Try to load existing model
            # If no model exists, train with default parameters
            self.model.fit([[0]])  # Placeholder training
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def _preprocess_transaction(self, transaction):
        # Convert transaction data to features
        features = [
            float(transaction['amount']),
            float(self._encode_category(transaction['category'])),
            float(self._encode_date(transaction['date']))
        ]
        return features
    
    def _encode_category(self, category):
        # Simple category encoding - you might want to make this more sophisticated
        categories = {
            'food': 1,
            'transport': 2,
            'entertainment': 3,
            'bills': 4,
            'other': 0
        }
        return categories.get(category.lower(), 0)
    
    def _encode_date(self, date_str):
        # Convert date to day of week (0-6)
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.weekday()

def detect_transaction_anomaly(transaction_data):
    """Main function to detect anomalies in transactions"""
    detector = AnomalyDetector()
    
    # Preprocess the transaction
    features = detector._preprocess_transaction(transaction_data)
    
    # Detect anomaly
    prediction = detector.model.predict([features])[0]
    score = detector.model.score_samples([features])[0]
    
    # Convert prediction to boolean and normalize score
    is_anomaly = prediction == -1
    confidence = 1 - (score + abs(detector.model.offset_)) / (2 * abs(detector.model.offset_))
    
    return is_anomaly, float(confidence)