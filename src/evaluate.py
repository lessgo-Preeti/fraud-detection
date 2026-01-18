"""
Model Evaluation Script
Provides detailed performance metrics and visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, f1_score
)
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from src.data_preprocessing import DataPreprocessor
from src.model import FraudDetectionModel


def plot_confusion_matrix(y_true, y_pred, save_path):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Confusion matrix saved to {save_path}")
    plt.close()


def plot_roc_curve(y_true, y_proba, save_path):
    """Plot ROC curve"""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"ROC curve saved to {save_path}")
    plt.close()


def plot_precision_recall_curve(y_true, y_proba, save_path):
    """Plot Precision-Recall curve"""
    precision, recall, _ = precision_recall_curve(y_true, y_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='blue', lw=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Precision-Recall curve saved to {save_path}")
    plt.close()


def evaluate_model():
    """
    Complete model evaluation pipeline
    """
    print("="*70)
    print(" CREDIT CARD FRAUD DETECTION - MODEL EVALUATION")
    print("="*70)
    
    config = Config()
    
    # Check if model exists
    if not os.path.exists(config.MODEL_SAVE_PATH):
        print("\nERROR: Trained model not found!")
        print(f"Please train the model first using: python src/train.py")
        return
    
    # Load data
    print("\nLoading and preprocessing data...")
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.prepare_data(balance_method='undersample')
    
    if X_train is None:
        print("\nERROR: Data preprocessing failed!")
        return
    
    # Load model
    print("\nLoading trained model...")
    fraud_model = FraudDetectionModel()
    fraud_model.load_model()
    
    # Make predictions
    print("\nMaking predictions on test set...")
    y_proba, y_pred = fraud_model.predict(X_test, threshold=0.5)
    
    # Evaluation metrics
    print("\n" + "="*70)
    print("EVALUATION METRICS")
    print("="*70)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Fraud']))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)
    print(f"\nTrue Negatives: {cm[0][0]}")
    print(f"False Positives: {cm[0][1]}")
    print(f"False Negatives: {cm[1][0]}")
    print(f"True Positives: {cm[1][1]}")
    
    # Additional metrics
    f1 = f1_score(y_test, y_pred)
    print(f"\nF1-Score: {f1:.4f}")
    
    # ROC-AUC
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    
    # Create visualizations
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    vis_dir = os.path.join(config.MODEL_DIR, 'visualizations')
    os.makedirs(vis_dir, exist_ok=True)
    
    plot_confusion_matrix(y_test, y_pred, os.path.join(vis_dir, 'confusion_matrix.png'))
    plot_roc_curve(y_test, y_proba, os.path.join(vis_dir, 'roc_curve.png'))
    plot_precision_recall_curve(y_test, y_proba, os.path.join(vis_dir, 'precision_recall_curve.png'))
    
    print("\n" + "="*70)
    print("EVALUATION COMPLETED!")
    print("="*70)
    print(f"\nVisualization saved in: {vis_dir}")


if __name__ == "__main__":
    evaluate_model()
