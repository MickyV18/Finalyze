from typing import Dict, List, Any
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pandas as pd
from app.config import supabase

class AnomalyDetector:
    def __init__(self):
        self.isolation_forest = IsolationForest(
            contamination=0.1,  # Expected proportion of anomalies
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.category_averages = {}
        self.category_std = {}  # Added to store standard deviation
        self.trained = False
        
    def _fetch_user_data(self, user_id: str) -> pd.DataFrame:
        """Fetch historical transaction data for specific user"""
        try:
            six_months_ago = (datetime.now() - timedelta(days=180)).isoformat()
            
            response = supabase.table('transactions')\
                .select('*')\
                .eq('user_id', user_id)\
                .gte('date', six_months_ago)\
                .execute()
                
            if not response.data:
                return pd.DataFrame()
                
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error fetching user data: {str(e)}")
            return pd.DataFrame()
    
    def _fetch_default_data(self) -> pd.DataFrame:
        """Fetch default transaction data from Supabase"""
        try:
            response = supabase.table('default_transactions')\
                .select('*')\
                .execute()
                
            if not response.data:
                return pd.DataFrame()
                
            return pd.DataFrame(response.data)
        except Exception as e:
            print(f"Error fetching default data: {str(e)}")
            return pd.DataFrame()
        
    def _prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for anomaly detection"""
        if df.empty:
            return np.array([])
            
        # Calculate category statistics
        category_stats = df.groupby('category')['amount'].agg(['mean', 'std']).to_dict('index')
        self.category_averages = {k: v['mean'] for k, v in category_stats.items()}
        self.category_std = {k: v['std'] for k, v in category_stats.items()}
        
        # Create features
        features = []
        for _, row in df.iterrows():
            category_avg = self.category_averages.get(row['category'], row['amount'])
            category_std = self.category_std.get(row['category'], row['amount'] * 0.1)  # Default 10% if no std
            
            # Calculate z-score
            z_score = (row['amount'] - category_avg) / category_std if category_std > 0 else 0
            
            date = pd.to_datetime(row['date'])
            day_of_week = date.dayofweek
            day_of_month = date.day
            
            feature_vector = [
                z_score,
                row['amount'],
                day_of_week / 7,
                day_of_month / 31
            ]
            features.append(feature_vector)
            
        return np.array(features)
        
    def train(self, user_id: str):
        """Train the anomaly detector on combined default and historical data"""
        # Fetch both default and user-specific data
        default_df = self._fetch_default_data()
        user_df = self._fetch_user_data(user_id)
        
        # Combine the datasets
        combined_df = pd.concat([default_df, user_df], ignore_index=True)
        
        if combined_df.empty:
            print("No training data available")
            return False
            
        # Prepare features from combined data
        features = self._prepare_features(combined_df)
        if len(features) == 0:
            return False
            
        # Fit scaler and model
        self.scaler.fit(features)
        normalized_features = self.scaler.transform(features)
        self.isolation_forest.fit(normalized_features)
        self.trained = True
        
        return True
        
    def analyze_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single transaction for anomalies"""
        user_id = transaction['user_id']
        
        # Train model if not already trained
        if not self.trained:
            self.train(user_id)
            
        # Get category statistics
        category_avg = self.category_averages.get(transaction['category'], transaction['amount'])
        category_std = self.category_std.get(transaction['category'], transaction['amount'] * 0.25)
        
        # Calculate z-score
        z_score = (transaction['amount'] - category_avg) / category_std if category_std > 0 else 0
        
        date = pd.to_datetime(transaction['date'])
        day_of_week = date.dayofweek
        day_of_month = date.day
        
        features = np.array([[
            z_score,
            transaction['amount'],
            day_of_week / 7,
            day_of_month / 31
        ]])
        
        # Normalize features
        normalized_features = self.scaler.transform(features)
        
        # Get anomaly score
        anomaly_score = self.isolation_forest.score_samples(normalized_features)[0]
        
        # Convert to probability-like score (0-100)
        confidence_score = (1 - (anomaly_score + 0.5)) * 100
        
        # Determine if transaction is anomalous based on z-score and confidence_score
        is_anomaly = False
        
        # Use z-score for initial anomaly detection
        if abs(z_score) <= 2:  # Within 2 standard deviations
            is_anomaly = False
        else:
            # If outside normal range, check confidence score
            is_anomaly = confidence_score > 70
        
        # Generate insights
        insights = self._generate_insights(
            transaction,
            category_avg,
            category_std,
            z_score,
            day_of_week,
            day_of_month
        )
        
        return {
            'is_anomaly': is_anomaly,
            'confidence_score': confidence_score,
            'insights': insights
        }
        
    def _generate_insights(
        self,
        transaction: Dict[str, Any],
        category_avg: float,
        category_std: float,
        z_score: float,
        day_of_week: int,
        day_of_month: int
    ) -> Dict[str, str]:
        """Generate human-readable insights about the transaction"""
        days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        
        # Format currency values
        formatted_avg = f"Rp {category_avg:,.0f}".replace(',', '.')
        formatted_std = f"Rp {category_std:,.0f}".replace(',', '.')
        
        # Generate amount analysis based on statistical significance
        if abs(z_score) <= 1:
            amount_analysis = f"Pengeluaran sangat normal untuk kategori ini (rata-rata: {formatted_avg})"
        elif abs(z_score) <= 2:
            if z_score > 0:
                amount_analysis = f"Pengeluaran sedikit lebih tinggi dari biasanya, tapi masih normal (rata-rata: {formatted_avg})"
            else:
                amount_analysis = f"Pengeluaran sedikit lebih rendah dari biasanya, tapi masih normal (rata-rata: {formatted_avg})"
        else:
            if z_score > 0:
                amount_analysis = f"Pengeluaran sangat tinggi dibanding rata-rata kategori yang sama (normal: {formatted_avg} ± {formatted_std})"
            else:
                amount_analysis = f"Pengeluaran sangat rendah dibanding rata-rata kategori yang sama (normal: {formatted_avg} ± {formatted_std})"
            
        timing_analysis = f"Transaksi dilakukan pada hari {days[day_of_week]}, tanggal {day_of_month}"
        category_frequency = f"Kategori: {transaction['category']}"
        
        return {
            'amount_analysis': amount_analysis,
            'timing_analysis': timing_analysis,
            'category_frequency': category_frequency,
            'category_avg': category_avg
        }

# Singleton instance
_detector = None

def get_anomaly_detector() -> AnomalyDetector:
    """Get or create the singleton anomaly detector instance"""
    global _detector
    if _detector is None:
        _detector = AnomalyDetector()
    return _detector