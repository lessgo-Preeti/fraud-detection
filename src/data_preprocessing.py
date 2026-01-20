"""
Data preprocessing module for Credit Card Fraud Detection
Handles data loading, cleaning, scaling, and splitting
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
import joblib
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


class DataPreprocessor:
    """
    Handles all data preprocessing operations
    """
    
    def __init__(self):
        self.config = Config()
        self.scaler = StandardScaler()
        
    def load_data(self, filepath=None):
        """
        Load the credit card dataset
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded dataset
        """
        if filepath is None:
            filepath = self.config.DATASET_PATH
            
        print(f"Loading data from {filepath}...")
        
        try:
            df = pd.read_csv(filepath)
            print(f"Data loaded successfully! Shape: {df.shape}")
            return df
        except FileNotFoundError:
            print(f"ERROR: Dataset not found at {filepath}")
            print("\nPlease download the dataset from:")
            print("https://www.kaggle.com/mlg-ulb/creditcardfraud")
            print(f"And place it in: {self.config.DATA_DIR}")
            return None
    
    def explore_data(self, df):
        """
        Display basic statistics and information about the dataset
        
        Args:
            df (pd.DataFrame): Dataset to explore
        """
        print("\n" + "="*50)
        print("DATASET EXPLORATION")
        print("="*50)
        
        print("\nDataset Info:")
        print(df.info())
        
        print("\nFirst 5 rows:")
        print(df.head())
        
        print("\nStatistical Summary:")
        print(df.describe())
        
        print("\nClass Distribution:")
        print(df['Class'].value_counts())
        
        fraud_percentage = (df['Class'].sum() / len(df)) * 100
        print(f"\nFraud Percentage: {fraud_percentage:.3f}%")
        
        print("\nMissing Values:")
        print(df.isnull().sum().sum())
        
    def handle_imbalance(self, df, method='undersample'):
        """
        Handle class imbalance in the dataset
        
        Args:
            df (pd.DataFrame): Input dataset
            method (str): 'undersample', 'oversample', or 'none'
            
        Returns:
            pd.DataFrame: Balanced dataset
        """
        if method == 'none':
            return df
        
        # Separate majority and minority classes
        df_majority = df[df['Class'] == 0]
        df_minority = df[df['Class'] == 1]
        
        print(f"\nOriginal class distribution:")
        print(f"Normal: {len(df_majority)}, Fraud: {len(df_minority)}")
        
        if method == 'undersample':
            # Undersample majority class
            df_majority_downsampled = resample(
                df_majority,
                replace=False,
                n_samples=len(df_minority) * 2,  # 2:1 ratio
                random_state=self.config.RANDOM_SEED
            )
            df_balanced = pd.concat([df_majority_downsampled, df_minority])
            
        elif method == 'oversample':
            # Oversample minority class
            df_minority_upsampled = resample(
                df_minority,
                replace=True,
                n_samples=len(df_majority) // 100,  # 1:100 ratio
                random_state=self.config.RANDOM_SEED
            )
            df_balanced = pd.concat([df_majority, df_minority_upsampled])
        
        print(f"Balanced class distribution:")
        print(f"Normal: {len(df_balanced[df_balanced['Class']==0])}, Fraud: {len(df_balanced[df_balanced['Class']==1])}")
        
        return df_balanced.sample(frac=1, random_state=self.config.RANDOM_SEED).reset_index(drop=True)
    
    def scale_features(self, X_train, X_test):
        """
        Standardize features using StandardScaler
        
        Args:
            X_train: Training features
            X_test: Testing features
            
        Returns:
            tuple: Scaled training and testing features
        """
        print("\nScaling features...")
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("Features scaled successfully!")
        
        return X_train_scaled, X_test_scaled
    
    def prepare_data(self, balance_method='undersample'):
        """
        Complete data preparation pipeline
        
        Args:
            balance_method (str): Method to handle class imbalance
            
        Returns:
            tuple: X_train, X_test, y_train, y_test
        """
        # Load data
        df = self.load_data()
        if df is None:
            return None, None, None, None
        
        # Explore data
        self.explore_data(df)
        
        # Handle imbalance
        df = self.handle_imbalance(df, method=balance_method)
        
        # Separate features and target
        X = df.drop('Class', axis=1)
        y = df['Class']
        
        # Split data
        print(f"\nSplitting data (test size: {self.config.TEST_SIZE})...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.config.TEST_SIZE,
            random_state=self.config.RANDOM_SEED,
            stratify=y
        )
        
        print(f"Training set size: {len(X_train)}")
        print(f"Testing set size: {len(X_test)}")
        
        # Scale features
        X_train_scaled, X_test_scaled = self.scale_features(X_train, X_test)
        
        # Save scaler
        os.makedirs(self.config.MODEL_DIR, exist_ok=True)
        joblib.dump(self.scaler, self.config.SCALER_SAVE_PATH)
        print(f"\nScaler saved to {self.config.SCALER_SAVE_PATH}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def load_scaler(self):
        """
        Load the saved scaler
        
        Returns:
            Scaler if successful
            
        Raises:
            FileNotFoundError: If scaler file not found
        """
        scaler_path = self.config.SCALER_SAVE_PATH
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler file not found at {scaler_path}")
        return joblib.load(scaler_path)


if __name__ == "__main__":
    # Test the preprocessing
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data()
    
    if X_train is not None:
        print("\n" + "="*50)
        print("Data preprocessing completed successfully!")
        print("="*50)
