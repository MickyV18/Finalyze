import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from datetime import datetime, timedelta
import joblib
import os
from typing import Dict, Tuple, List, Optional
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedAnomalyDetector:
    def __init__(self, model_path: str = "models/enhanced_isolation_forest.joblib"):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.preprocessor = None
        self.categories = {
            'food': 1,
            'transport': 2,
            'entertainment': 3,
            'bills': 4,
            'other': 0
        }
        self.historical_stats = {}
        self._initialize_model()
    
    def _load_food_prices(self) -> Dict[str, float]:
        """Load average food prices from CSV"""
        try:
            # Update path to be relative to the script location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, 'Rata-rata Harga.csv')
            df = pd.read_csv(file_path)
            # Create a dictionary of food name to price
            prices = dict(zip(df['Nama'].str.lower(), df['2017']))
            return prices
        except Exception as e:
            logger.error(f"Error loading food prices: {e}")
            return {}
    
    def _initialize_model(self):
        """Initialize model with advanced preprocessing pipeline"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            if os.path.exists(self.model_path):
                try:
                    saved_data = joblib.load(self.model_path)
                    self.model = saved_data['model']
                    self.preprocessor = saved_data['preprocessor']
                    self.historical_stats = saved_data.get('historical_stats', {})
                    logger.info("Model and preprocessor loaded successfully")
                except Exception as e:
                    logger.warning(f"Error loading existing model: {e}")
                    logger.info("Training new model instead")
                    self._initialize_new_model()
            else:
                logger.info("No existing model found. Training new model...")
                self._initialize_new_model()
                
        except Exception as e:
            logger.error(f"Error initializing model: {e}")
            raise ValueError("Failed to initialize model")

    def _initialize_new_model(self):
        """Initialize a new model with default settings"""
        try:
            # Create preprocessing pipeline
            numeric_features = ['amount', 'day_of_week', 'day_of_month', 'month']
            categorical_features = ['category']
            
            numeric_transformer = Pipeline(steps=[
                ('scaler', StandardScaler())
            ])
            
            # Updated OneHotEncoder to use sparse_output instead of sparse
            categorical_transformer = Pipeline(steps=[
                ('onehot', OneHotEncoder(drop='first', sparse_output=False))
            ])
            
            self.preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numeric_transformer, numeric_features),
                    ('cat', categorical_transformer, categorical_features)
                ])
            
            self.model = IsolationForest(
                contamination=0.1,
                n_estimators=200,
                max_samples='auto',
                bootstrap=True,
                n_jobs=-1,
                random_state=42
            )
            
            # Train with default data
            self._train_with_default_data()
            
            # Save the newly initialized model
            self._save_model()
            logger.info("New model initialized and saved successfully")
            
        except Exception as e:
            logger.error(f"Error initializing new model: {e}")
            raise ValueError("Failed to initialize new model")

    def _save_model(self):
        """Save the current model state"""
        try:
            joblib.dump({
                'model': self.model,
                'preprocessor': self.preprocessor,
                'historical_stats': self.historical_stats
            }, self.model_path)
            logger.info("Model saved successfully")
        except Exception as e:
            logger.warning(f"Warning: Could not save model: {e}")
    
    def _train_with_default_data(self):
        """Train model with diverse default data"""
        default_data = self._generate_default_data()
        self.train(default_data)
    
    def _generate_default_data(self) -> List[Dict]:
        """Generate diverse default training data"""
        data = []
        categories = list(self.categories.keys())
        start_date = datetime.now() - timedelta(days=365)
        food_prices = self._load_food_prices()
        
        # Generate normal transactions
        for _ in range(1000):
            date = start_date + timedelta(days=np.random.randint(0, 365))
            category = np.random.choice(categories)
            
            if category == 'food':
                # Get price variation for each food item
                for food_name, base_price in food_prices.items():
                    # Add multiple transactions for each food item
                    for _ in range(5):
                        # Allow 30% variation from base price
                        amount = np.random.uniform(base_price * 0.7, base_price * 1.3)
                        data.append({
                            'amount': max(1000, amount),
                            'category': category,
                            'date': date.strftime('%Y-%m-%d'),
                            'description': food_name
                        })
            else:
                # Other categories remain the same
                if category == 'transport':
                    amount = np.random.normal(30000, 10000)
                elif category == 'entertainment':
                    amount = np.random.normal(100000, 30000)
                elif category == 'bills':
                    amount = np.random.normal(500000, 100000)
                else:
                    amount = np.random.normal(75000, 25000)
                
                data.append({
                    'amount': max(1000, amount),
                    'category': category,
                    'date': date.strftime('%Y-%m-%d'),
                    'description': category
                })
        
        # Add fewer anomalies for better balance
        anomaly_count = len(data) // 20  # 5% anomalies
        for _ in range(anomaly_count):
            date = start_date + timedelta(days=np.random.randint(0, 365))
            category = np.random.choice(categories)
            # Anomalies are now relative to category averages
            if category == 'food':
                amount = np.random.choice(list(food_prices.values())) * 5  # 5x normal price
            else:
                amount = np.random.normal(1000000, 500000)
            
            data.append({
                'amount': max(1000, amount),
                'category': category,
                'date': date.strftime('%Y-%m-%d'),
                'description': category
            })
            
        return data
    
    def _extract_advanced_features(self, transactions: List[Dict]) -> pd.DataFrame:
        """Extract advanced features from transactions"""
        try:
            df = pd.DataFrame(transactions)
            df['date'] = pd.to_datetime(df['date'])
            
            # Basic features
            df['day_of_week'] = df['date'].dt.dayofweek
            df['day_of_month'] = df['date'].dt.day
            df['month'] = df['date'].dt.month
            
            # Amount features
            df['amount_log'] = np.log1p(df['amount'])
            
            # Category encoding
            df['category'] = df['category'].str.lower()
            
            return df
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            raise ValueError("Failed to extract features from transactions")
        
    def _fetch_historical_data(self) -> List[Dict]:
        """Fetch historical transactions from database"""
        try:
            from app.config import supabase
            
            response = supabase.table('transactions')\
                .select('amount, category, date, description')\
                .execute()
            
            return response.data
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return []
    
    def train(self, transactions: List[Dict]) -> bool:
        """Train the model with historical transactions"""
        try:
            # Get historical data from database
            historical_data = self._fetch_historical_data()
            
            # Combine with new transactions
            all_transactions = historical_data + transactions
            
            if not all_transactions:
                logger.warning("No transactions available for training")
                return False
            
            # Process data
            df = self._extract_advanced_features(all_transactions)
            
            # Update historical stats
            self._update_historical_stats(df)
            
            # Prepare features for training
            features_df = df[['amount', 'day_of_week', 'day_of_month', 'month', 'category']]
            
            # Fit preprocessor and transform data
            X = self.preprocessor.fit_transform(features_df)
            
            # Train model
            self.model.fit(X)
            
            # Save model
            self._save_model()
            
            logger.info(f"Model trained successfully with {len(all_transactions)} transactions")
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False
    
    def _update_historical_stats(self, df: pd.DataFrame):
        """Update historical statistics for better analysis"""
        try:
            self.historical_stats = {
                'amount_stats': {
                    'mean': df.groupby('category')['amount'].mean().to_dict(),
                    'std': df.groupby('category')['amount'].std().to_dict(),
                    'median': df.groupby('category')['amount'].median().to_dict(),
                    'q1': df.groupby('category')['amount'].quantile(0.25).to_dict(),
                    'q3': df.groupby('category')['amount'].quantile(0.75).to_dict()
                },
                'category_frequency': df['category'].value_counts().to_dict(),
                'day_of_week_stats': df.groupby('day_of_week')['amount'].mean().to_dict(),
                'day_of_month_stats': df.groupby('day_of_month')['amount'].mean().to_dict()
            }
        except Exception as e:
            logger.error(f"Error updating historical stats: {e}")
            raise ValueError("Failed to update historical statistics")
    
    def analyze_transaction(self, transaction: Dict) -> Dict:
        """Analyze a transaction with enhanced insights and normalized confidence score"""
        if self.model is None:
            raise ValueError("Model not initialized")
        
        try:
            # For food transactions, load reference prices
            if transaction['category'].lower() == 'food':
                food_prices = self._load_food_prices()
                description = transaction['description'].lower()
                if description in food_prices:
                    base_price = food_prices[description]
                    # If price is within 50% of reference, treat as normal
                    if 0.5 * base_price <= float(transaction['amount']) <= 1.5 * base_price:
                        return {
                            'is_anomaly': False,
                            'confidence_score': 0.0,
                            'insights': {
                                'amount_analysis': f"Normal amount for {description}",
                                'timing_analysis': self._get_timing_insight(transaction['date']),
                                'category_analysis': "Food category with verified price"
                            }
                        }

            # Continue with regular analysis for other cases
            df = self._extract_advanced_features([transaction])
            features_df = df[['amount', 'day_of_week', 'day_of_month', 'month', 'category']]
            X = self.preprocessor.transform(features_df)
            
            is_anomaly = self.model.predict(X)[0] == -1
            raw_score = self.model.score_samples(X)[0]
            
            # Calculate z-score for amount analysis
            category = transaction['category']
            amount = float(transaction['amount'])
            if category in self.historical_stats['amount_stats']['mean']:
                mean = self.historical_stats['amount_stats']['mean'][category]
                std = self.historical_stats['amount_stats']['std'][category]
                if std > 0:
                    z_score = (amount - mean) / std
                else:
                    z_score = 0
            else:
                z_score = 0
            
            min_score = -0.5
            max_score = 0.5
            score_range = max_score - min_score
            
            if is_anomaly:
                normalized_score = ((raw_score - max_score) / score_range) * -100
                confidence = min(max(normalized_score, 0), 100)
            else:
                normalized_score = ((raw_score - min_score) / score_range) * 100
                confidence = min(max(normalized_score, 0), 100)
            
            insights = {
                'amount_analysis': self._get_amount_insight(amount, category, z_score),
                'timing_analysis': self._get_timing_insight(transaction['date']),
                'category_analysis': self._get_category_insight(category)
            }
            
            return {
                'is_anomaly': is_anomaly,
                'confidence_score': confidence,
                'insights': insights
            }
            
        except Exception as e:
            logger.error(f"Error analyzing transaction: {e}")
            raise ValueError("Failed to analyze transaction")
    
    def _get_amount_insight(self, amount: float, category: str, z_score: float) -> str:
        """Generate detailed amount insight"""
        try:
            cat_stats = self.historical_stats['amount_stats']
            if category in cat_stats['mean']:
                if abs(z_score) > 3:
                    return f"Highly unusual amount for {category} (>{abs(z_score)}σ from mean)"
                elif abs(z_score) > 2:
                    return f"Unusual amount for {category} ({abs(z_score):.1f}σ from mean)"
                else:
                    return f"Normal amount for {category}"
            return "Insufficient historical data for category comparison"
        except Exception as e:
            logger.error(f"Error generating amount insight: {e}")
            return "Error analyzing amount"
    
    def _get_timing_insight(self, date_str: str) -> str:
        """Generate detailed timing insight"""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            day_stats = self.historical_stats.get('day_of_week_stats', {})
            
            if day_stats:
                avg_amount = day_stats.get(date.weekday(), 0)
                if date.weekday() >= 5:
                    return f"Weekend transaction (avg. amount for this day: {avg_amount:,.0f})"
                return f"Weekday transaction (avg. amount for this day: {avg_amount:,.0f})"
            return "Insufficient historical data for timing analysis"
        except Exception as e:
            logger.error(f"Error generating timing insight: {e}")
            return "Error analyzing timing"
    
    def _get_category_insight(self, category: str) -> str:
        """Generate detailed category insight"""
        try:
            freq = self.historical_stats.get('category_frequency', {})
            if category in freq:
                total = sum(freq.values())
                category_percent = (freq[category] / total) * 100
                return f"Category represents {category_percent:.1f}% of all transactions"
            return "New category with no historical data"
        except Exception as e:
            logger.error(f"Error generating category insight: {e}")
            return "Error analyzing category"

# Singleton instance
_detector = None

def get_anomaly_detector():
    """Factory function to get anomaly detector instance"""
    global _detector
    if _detector is None:
        _detector = EnhancedAnomalyDetector()
    return _detector