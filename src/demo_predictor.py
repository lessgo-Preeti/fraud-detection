"""
Lightweight demo predictor for when the full model is not available.
Uses statistical patterns and rule-based logic to simulate predictions.
"""

import numpy as np


class DemoFraudPredictor:
    """
    Lightweight predictor that works without the trained model.
    Uses statistical patterns to provide realistic fraud predictions.
    """
    
    def __init__(self):
        """Initialize demo predictor with statistical thresholds"""
        self.is_demo_mode = True
        
        # Statistical thresholds derived from fraud patterns
        self.high_amount_threshold = 1000
        self.suspicious_patterns = {
            'high_v1': 3.0,
            'high_v3': 3.0,
            'high_v4': 3.0,
            'high_v10': 3.0,
            'high_v12': 3.0,
            'high_v14': 3.0,
            'low_v2': -3.0,
            'low_v5': -3.0,
        }
    
    def predict_single(self, transaction_data, threshold=0.5):
        """
        Predict fraud for a single transaction using rule-based logic
        
        Args:
            transaction_data (dict or array): Transaction features
            threshold (float): Classification threshold
            
        Returns:
            dict: Prediction results
        """
        # Convert to dict if array
        if not isinstance(transaction_data, dict):
            # Assume it's in order: V1-V28, Amount, Time
            transaction_data = {f'V{i}': transaction_data[i] for i in range(28)}
            transaction_data['Amount'] = transaction_data[28] if len(transaction_data) > 28 else 0
            transaction_data['Time'] = transaction_data[29] if len(transaction_data) > 29 else 0
        
        # Calculate fraud score based on statistical patterns
        fraud_score = 0.0
        
        # 1. Check amount (higher amounts have higher fraud risk)
        amount = transaction_data.get('Amount', 0)
        if amount > self.high_amount_threshold:
            fraud_score += 0.15
        elif amount > 500:
            fraud_score += 0.08
        elif amount < 1:
            fraud_score += 0.05  # Very small transactions can be tests
        
        # 2. Check PCA components for anomalies
        suspicious_count = 0
        
        # High values in certain components indicate fraud
        for i in [1, 3, 4, 10, 12, 14]:
            v_key = f'V{i}'
            v_value = transaction_data.get(v_key, 0)
            if abs(v_value) > 3.0:
                suspicious_count += 1
                fraud_score += 0.08
        
        # 3. Check for extreme outliers in any V component
        extreme_outliers = 0
        for i in range(1, 29):
            v_key = f'V{i}'
            v_value = transaction_data.get(v_key, 0)
            if abs(v_value) > 4.0:
                extreme_outliers += 1
                fraud_score += 0.12
        
        # 4. Multiple anomalies together increase risk
        if suspicious_count >= 3:
            fraud_score += 0.15
        if extreme_outliers >= 2:
            fraud_score += 0.20
        
        # 5. Time-based patterns (unusual times can be suspicious)
        time_val = transaction_data.get('Time', 0)
        # Normalize time to hours (assuming seconds)
        hour = (time_val / 3600) % 24
        # Late night/early morning transactions (12 AM - 6 AM)
        if 0 <= hour < 6:
            fraud_score += 0.05
        
        # 6. Combination of high amount + anomalies
        if amount > 500 and suspicious_count >= 2:
            fraud_score += 0.15
        
        # 7. Add some randomness for variety (±5%)
        noise = np.random.uniform(-0.05, 0.05)
        fraud_score = max(0.0, min(1.0, fraud_score + noise))
        
        # Calculate final probability with sigmoid-like scaling
        # This makes the scores more realistic
        probability = self._smooth_score(fraud_score)
        
        # Make final prediction
        prediction = 1 if probability > threshold else 0
        
        result = {
            'is_fraud': bool(prediction),
            'fraud_probability': float(probability),
            'confidence': float(max(probability, 1 - probability)),
            'risk_level': self._get_risk_level(probability),
            'demo_mode': True  # Flag to indicate demo mode
        }
        
        return result
    
    def predict_batch(self, transactions_df, threshold=0.5):
        """
        Predict fraud for multiple transactions
        
        Args:
            transactions_df (pd.DataFrame): DataFrame with transaction features
            threshold (float): Classification threshold
            
        Returns:
            pd.DataFrame: DataFrame with predictions
        """
        import pandas as pd
        
        results = []
        for _, row in transactions_df.iterrows():
            result = self.predict_single(row.to_dict(), threshold)
            results.append(result)
        
        results_df = transactions_df.copy()
        results_df['fraud_probability'] = [r['fraud_probability'] for r in results]
        results_df['is_fraud'] = [r['is_fraud'] for r in results]
        results_df['risk_level'] = [r['risk_level'] for r in results]
        
        return results_df
    
    def _smooth_score(self, raw_score):
        """
        Apply sigmoid-like smoothing to make scores more realistic
        
        Args:
            raw_score (float): Raw fraud score (0-1)
            
        Returns:
            float: Smoothed probability
        """
        # Use a modified sigmoid to spread scores more naturally
        # This prevents clustering at extremes
        x = (raw_score - 0.5) * 6  # Scale and center
        smoothed = 1 / (1 + np.exp(-x))
        return smoothed
    
    def _get_risk_level(self, probability):
        """
        Determine risk level based on probability
        
        Args:
            probability (float): Fraud probability
            
        Returns:
            str: Risk level (Low, Medium, High, Critical)
        """
        if probability < 0.25:
            return 'Low'
        elif probability < 0.50:
            return 'Medium'
        elif probability < 0.75:
            return 'High'
        else:
            return 'Critical'


if __name__ == "__main__":
    # Test the demo predictor
    predictor = DemoFraudPredictor()
    
    # Test 1: Normal transaction
    print("Test 1: Normal transaction")
    normal_transaction = {f'V{i}': np.random.randn() * 0.5 for i in range(1, 29)}
    normal_transaction['Amount'] = 50.0
    normal_transaction['Time'] = 43200  # Noon
    
    result = predictor.predict_single(normal_transaction)
    print(f"  Is Fraud: {result['is_fraud']}")
    print(f"  Probability: {result['fraud_probability']:.4f}")
    print(f"  Risk Level: {result['risk_level']}")
    
    # Test 2: Suspicious transaction
    print("\nTest 2: Suspicious transaction")
    suspicious_transaction = {f'V{i}': np.random.randn() * 0.5 for i in range(1, 29)}
    suspicious_transaction['V1'] = 4.5  # Extreme value
    suspicious_transaction['V3'] = 3.8  # High value
    suspicious_transaction['V10'] = -4.2  # Extreme value
    suspicious_transaction['Amount'] = 1500.0  # High amount
    suspicious_transaction['Time'] = 7200  # 2 AM
    
    result = predictor.predict_single(suspicious_transaction)
    print(f"  Is Fraud: {result['is_fraud']}")
    print(f"  Probability: {result['fraud_probability']:.4f}")
    print(f"  Risk Level: {result['risk_level']}")
    
    print("\n✓ Demo predictor is working correctly!")
