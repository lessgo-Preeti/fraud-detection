"""
Training script for Credit Card Fraud Detection Model
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from src.data_preprocessing import DataPreprocessor
from src.model import FraudDetectionModel


def plot_training_history(history, save_path):
    """
    Plot training history
    
    Args:
        history: Training history object
        save_path: Path to save the plot
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Loss
    axes[0, 0].plot(history.history['loss'], label='Training Loss')
    axes[0, 0].plot(history.history['val_loss'], label='Validation Loss')
    axes[0, 0].set_title('Model Loss')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Loss')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Accuracy
    axes[0, 1].plot(history.history['accuracy'], label='Training Accuracy')
    axes[0, 1].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0, 1].set_title('Model Accuracy')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Accuracy')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Precision
    axes[1, 0].plot(history.history['precision'], label='Training Precision')
    axes[1, 0].plot(history.history['val_precision'], label='Validation Precision')
    axes[1, 0].set_title('Model Precision')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Precision')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Recall
    axes[1, 1].plot(history.history['recall'], label='Training Recall')
    axes[1, 1].plot(history.history['val_recall'], label='Validation Recall')
    axes[1, 1].set_title('Model Recall')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Recall')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"\nTraining history plot saved to {save_path}")
    plt.close()


def main():
    """
    Main training pipeline
    """
    print("="*70)
    print(" CREDIT CARD FRAUD DETECTION - TRAINING PIPELINE")
    print("="*70)
    
    # Initialize config
    config = Config()
    
    # Create necessary directories
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    
    # Step 1: Data Preprocessing
    print("\nSTEP 1: Data Preprocessing")
    print("-" * 70)
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(balance_method='undersample')
    
    if X_train is None:
        print("\nERROR: Data preprocessing failed!")
        print("Please ensure the dataset is available.")
        return
    
    # Step 2: Build and Train Model
    print("\nSTEP 2: Model Building and Training")
    print("-" * 70)
    fraud_model = FraudDetectionModel()
    fraud_model.build_model()
    
    # Train the model
    history = fraud_model.train(X_train, y_train)
    
    # Save training history
    joblib.dump(history.history, config.HISTORY_SAVE_PATH)
    print(f"\nTraining history saved to {config.HISTORY_SAVE_PATH}")
    
    # Step 3: Plot training history
    print("\nSTEP 3: Visualizing Training History")
    print("-" * 70)
    plot_path = os.path.join(config.MODEL_DIR, 'training_history.png')
    plot_training_history(history, plot_path)
    
    # Step 4: Evaluate on test set
    print("\nSTEP 4: Evaluating on Test Set")
    print("-" * 70)
    test_results = fraud_model.model.evaluate(X_test, y_test, verbose=1)
    
    print("\n" + "="*70)
    print("FINAL TEST RESULTS")
    print("="*70)
    print(f"Test Loss: {test_results[0]:.4f}")
    print(f"Test Accuracy: {test_results[1]:.4f}")
    print(f"Test Precision: {test_results[2]:.4f}")
    print(f"Test Recall: {test_results[3]:.4f}")
    print(f"Test AUC: {test_results[4]:.4f}")
    
    print("\n" + "="*70)
    print("TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"\nModel saved to: {config.MODEL_SAVE_PATH}")
    print(f"Scaler saved to: {config.SCALER_SAVE_PATH}")
    print("\nYou can now:")
    print("1. Run evaluation: python src/evaluate.py")
    print("2. Start web app: python web/app.py")
    print("="*70)


if __name__ == "__main__":
    main()
