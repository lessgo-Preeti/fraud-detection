"""
Flask Web Application for Credit Card Fraud Detection System
Provides web interface for uploading transactions and viewing predictions
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import numpy as np
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

# Import demo predictor first (no TensorFlow dependency)
from src.demo_predictor import DemoFraudPredictor

from database.db_operations import DatabaseOperations
from database.db_setup import create_database, Base

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize predictor (lazy loading)
predictor = None

# CRITICAL: Create database tables on startup
print("\n" + "="*70)
print("INITIALIZING APPLICATION")
print("="*70)
try:
    create_database()
except Exception as e:
    print(f"WARNING: Database setup issue: {e}")
    print("Attempting to continue anyway...")
    # Try to create tables without failing
    try:
        from sqlalchemy import create_engine
        from database.db_setup import Base
        config = Config()
        engine = create_engine(config.DATABASE_URI)
        Base.metadata.create_all(engine)
        print("✓ Database tables created successfully")
    except Exception as e2:
        print(f"ERROR: Could not create database tables: {e2}")
        print("NOTE: Database operations may fail!")
print("="*70 + "\n")

def get_predictor():
    """Get or initialize predictor - guaranteed to return a working predictor"""
    global predictor
    if predictor is None:
        # Check if model files exist first
        config = Config()
        model_exists = os.path.exists(config.MODEL_PATH)
        scaler_exists = os.path.exists(config.SCALER_PATH)
        
        # Use demo mode if files don't exist
        if not model_exists or not scaler_exists:
            print("🔄 Using DEMO MODE (model files not available)")
            # Create a simple wrapper for demo predictor
            class DemoWrapper:
                def __init__(self):
                    self.demo_predictor = DemoFraudPredictor()
                    self.is_demo_mode = True
                    self.model = None
                    self.scaler = None
                
                def predict_single(self, transaction_data, threshold=0.5):
                    return self.demo_predictor.predict_single(transaction_data, threshold)
                
                def predict_batch(self, transactions_df, threshold=0.5):
                    return self.demo_predictor.predict_batch(transactions_df, threshold)
            
            predictor = DemoWrapper()
            print("✓ Demo mode predictor ready")
        else:
            # Try to import and use full model (lazy import)
            try:
                print("Loading full model...")
                from src.predict import FraudPredictor
                predictor = FraudPredictor()
                predictor.load_model_and_scaler()
            except Exception as e:
                print(f"⚠️  Error loading full model: {e}")
                print("🔄 Falling back to demo mode...")
                class DemoWrapper:
                    def __init__(self):
                        self.demo_predictor = DemoFraudPredictor()
                        self.is_demo_mode = True
                        self.model = None
                        self.scaler = None
                    
                    def predict_single(self, transaction_data, threshold=0.5):
                        return self.demo_predictor.predict_single(transaction_data, threshold)
                    
                    def predict_batch(self, transactions_df, threshold=0.5):
                        return self.demo_predictor.predict_batch(transactions_df, threshold)
                
                predictor = DemoWrapper()
                print("✓ Demo mode predictor ready")
    return predictor


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction page"""
    if request.method == 'POST':
        try:
            # Get transaction data from form or JSON
            if request.is_json:
                data = request.json
            else:
                data = request.form.to_dict()
            
            # Convert to proper format
            transaction_data = {}
            for i in range(1, 29):
                key = f'V{i}'
                transaction_data[key] = float(data.get(key, 0))
            transaction_data['Amount'] = float(data.get('Amount', 0))
            transaction_data['Time'] = float(data.get('Time', 0))
            
            # Make prediction
            pred = get_predictor()
            result = pred.predict_single(transaction_data)
            
            # Save to database
            db_ops = DatabaseOperations()
            transaction_db_data = {**transaction_data}
            for i in range(1, 29):
                transaction_db_data[f'v{i}'] = transaction_data[f'V{i}']
                del transaction_db_data[f'V{i}']
            transaction_db_data['time'] = transaction_data['Time']
            transaction_db_data['amount'] = transaction_data['Amount']
            del transaction_db_data['Time']
            del transaction_db_data['Amount']
            transaction_db_data.update({
                'is_fraud': result['is_fraud'],
                'fraud_probability': result['fraud_probability'],
                'risk_level': result['risk_level']
            })
            
            transaction = db_ops.add_transaction(transaction_db_data)
            
            # Log prediction
            log_data = {
                'transaction_id': transaction.id,
                'is_fraud': result['is_fraud'],
                'fraud_probability': result['fraud_probability'],
                'risk_level': result['risk_level'],
                'model_version': '1.0'
            }
            db_ops.add_prediction_log(log_data)
            db_ops.close()
            
            # Return result
            if request.is_json:
                return jsonify(result)
            else:
                return render_template('result.html', result=result, transaction=transaction_data)
        
        except Exception as e:
            error_msg = str(e)
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            else:
                return render_template('error.html', error=error_msg)
    
    return render_template('predict.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page with statistics"""
    db_ops = DatabaseOperations()
    stats = db_ops.get_statistics()
    recent_transactions = db_ops.get_all_transactions(limit=10)
    db_ops.close()
    
    return render_template('dashboard.html', stats=stats, transactions=recent_transactions)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.json
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Make prediction
        pred = get_predictor()
        result = pred.predict_single(data)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    db_ops = DatabaseOperations()
    stats = db_ops.get_statistics()
    db_ops.close()
    
    return jsonify(stats)


@app.route('/api/transactions')
def api_transactions():
    """API endpoint to get recent transactions"""
    limit = request.args.get('limit', 10, type=int)
    
    db_ops = DatabaseOperations()
    transactions = db_ops.get_all_transactions(limit=limit)
    db_ops.close()
    
    transactions_data = []
    for t in transactions:
        transactions_data.append({
            'id': t.id,
            'amount': t.amount,
            'time': t.time,
            'is_fraud': t.is_fraud,
            'fraud_probability': t.fraud_probability,
            'risk_level': t.risk_level,
            'created_at': t.created_at.isoformat() if t.created_at else None
        })
    
    return jsonify(transactions_data)


@app.route('/health')
def health():
    """Health check endpoint"""
    pred = get_predictor()
    status_info = {
        'status': 'healthy', 
        'service': 'fraud-detection',
        'demo_mode': pred.is_demo_mode if pred else False
    }
    return jsonify(status_info)


if __name__ == '__main__':
    # Ensure database exists
    print("Checking database...")
    try:
        create_database()
    except Exception as e:
        print(f"Database already exists or error: {e}")
    
    # Run app
    config = Config()
    print(f"\n{'='*70}")
    print("FRAUD DETECTION WEB APPLICATION")
    print(f"{'='*70}")
    print(f"\nStarting server on http://{config.FLASK_HOST}:{config.FLASK_PORT}")
    print(f"Debug mode: {config.DEBUG}")
    print("\nAvailable endpoints:")
    print("  - http://localhost:5000/          (Home)")
    print("  - http://localhost:5000/predict   (Prediction form)")
    print("  - http://localhost:5000/dashboard (Statistics)")
    print("  - http://localhost:5000/api/predict (API endpoint)")
    print(f"{'='*70}\n")
    
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.DEBUG
    )
