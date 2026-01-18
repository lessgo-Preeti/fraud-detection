"""
Prediction module for making fraud predictions on new transactions
"""

import numpy as np
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from src.model import FraudDetectionModel
from src.data_preprocessing import DataPreprocessor


class FraudPredictor:
    """
    Handles predictions for new transactions
    """
    
    def __init__(self):
        self.config = Config()
        self.model = None
        self.scaler = None
        
    def load_model_and_scaler(self):
        """Load the trained model and scaler"""
        print("Loading model and scaler...")
        
        # Load model
        fraud_model = FraudDetectionModel()
        self.model = fraud_model.load_model()
        
        # Load scaler
        preprocessor = DataPreprocessor()
        self.scaler = preprocessor.load_scaler()
        
        print("Model and scaler loaded successfully!")
    
    def predict_single(self, transaction_data, threshold=0.5):
        """
        Predict fraud for a single transaction
        
        Args:
            transaction_data (dict or array): Transaction features
            threshold (float): Classification threshold
            
        Returns:
            dict: Prediction results
        """
        if self.model is None or self.scaler is None:
            self.load_model_and_scaler()
        
        # Convert to numpy array if dict
        if isinstance(transaction_data, dict):
            # Ensure correct order of features (same as training: Time, V1-V28, Amount)
            feature_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
            transaction_array = np.array([transaction_data.get(col, 0) for col in feature_cols])
        else:
            transaction_array = np.array(transaction_data)
        
        # Reshape for single prediction
        transaction_array = transaction_array.reshape(1, -1)
        
        # Scale features
        transaction_scaled = self.scaler.transform(transaction_array)
        
        # Make prediction
        probability = self.model.predict(transaction_scaled)[0][0]
        prediction = 1 if probability > threshold else 0
        
        result = {
            'is_fraud': bool(prediction),
            'fraud_probability': float(probability),
            'confidence': float(max(probability, 1 - probability)),
            'risk_level': self._get_risk_level(probability)
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
        if self.model is None or self.scaler is None:
            self.load_model_and_scaler()
        
        # Scale features
        transactions_scaled = self.scaler.transform(transactions_df)
        
        # Make predictions
        probabilities = self.model.predict(transactions_scaled)
        predictions = (probabilities > threshold).astype(int)
        
        # Create results dataframe
        results_df = transactions_df.copy()
        results_df['fraud_probability'] = probabilities
        results_df['is_fraud'] = predictions
        results_df['risk_level'] = results_df['fraud_probability'].apply(self._get_risk_level)
        
        return results_df
    
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
    # Example usage
    predictor = FraudPredictor()
    
    # Example transaction (random values for demonstration)
    example_transaction = {f'V{i}': np.random.randn() for i in range(1, 29)}
    example_transaction['Amount'] = 100.50
    example_transaction['Time'] = 3600
    
    print("Making prediction for example transaction...")
    result = predictor.predict_single(example_transaction)
    
    print("\nPrediction Results:")
    print(f"Is Fraud: {result['is_fraud']}")
    print(f"Probability: {result['fraud_probability']:.4f}")
    print(f"Confidence: {result['confidence']:.4f}")
    print(f"Risk Level: {result['risk_level']}")
