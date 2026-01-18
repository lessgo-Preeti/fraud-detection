"""
Configuration file for the Credit Card Fraud Detection System
"""
import os

class Config:
    # Project paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    
    # Dataset
    DATASET_PATH = os.path.join(DATA_DIR, 'creditcard.csv')
    
    # Model parameters
    RANDOM_SEED = 42
    TEST_SIZE = 0.2
    VALIDATION_SPLIT = 0.2
    
    # Neural Network Architecture
    INPUT_DIM = 30
    HIDDEN_LAYERS = [64, 32]
    DROPOUT_RATE = 0.3
    L2_REGULARIZATION = 0.001
    
    # Training parameters
    EPOCHS = 50
    BATCH_SIZE = 256
    LEARNING_RATE = 0.001
    EARLY_STOPPING_PATIENCE = 10
    
    # Database configuration
    DB_TYPE = 'sqlite'  # Change to 'postgresql' for production
    
    # SQLite (for development)
    SQLITE_DB_PATH = os.path.join(BASE_DIR, 'fraud_detection.db')
    
    # PostgreSQL (for production)
    POSTGRES_USER = os.getenv('DB_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    POSTGRES_HOST = os.getenv('DB_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('DB_PORT', '5432')
    POSTGRES_DB = os.getenv('DB_NAME', 'fraud_detection')
    
    @property
    def DATABASE_URI(self):
        if self.DB_TYPE == 'postgresql':
            return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        else:
            return f'sqlite:///{self.SQLITE_DB_PATH}'
    
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    DEBUG = True
    
    # Model saving
    MODEL_SAVE_PATH = os.path.join(MODEL_DIR, 'fraud_detection_model.h5')
    SCALER_SAVE_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
    HISTORY_SAVE_PATH = os.path.join(MODEL_DIR, 'training_history.pkl')
