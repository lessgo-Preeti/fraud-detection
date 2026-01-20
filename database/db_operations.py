"""
Database operations module
Handles CRUD operations for transactions and predictions
"""

from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_setup import Transaction, PredictionLog, User, get_session, create_database, Base
from sqlalchemy import create_engine
from config import Config

# Ensure tables exist when module is loaded
_tables_ensured = False

def ensure_tables_exist():
    """Make absolutely sure tables exist before any operation"""
    global _tables_ensured
    if not _tables_ensured:
        try:
            config = Config()
            engine = create_engine(config.DATABASE_URI)
            Base.metadata.create_all(engine, checkfirst=True)
            _tables_ensured = True
            print("✓ Database tables verified/created")
        except Exception as e:
            print(f"WARNING: Could not ensure tables exist: {e}")


class DatabaseOperations:
    """
    Handles all database operations
    """
    
    def __init__(self):
        ensure_tables_exist()  # Make sure tables exist before ANY operation
        self.session = get_session()
    
    def add_transaction(self, transaction_data):
        """
        Add a new transaction to the database
        
        Args:
            transaction_data (dict): Transaction details
            
        Returns:
            Transaction: Created transaction object
        """
        transaction = Transaction(**transaction_data)
        self.session.add(transaction)
        self.session.commit()
        return transaction
    
    def get_transaction(self, transaction_id):
        """
        Get a transaction by ID
        
        Args:
            transaction_id (int): Transaction ID
            
        Returns:
            Transaction: Transaction object or None
        """
        return self.session.query(Transaction).filter_by(id=transaction_id).first()
    
    def get_all_transactions(self, limit=100):
        """
        Get all transactions
        
        Args:
            limit (int): Maximum number of transactions to return
            
        Returns:
            list: List of Transaction objects
        """
        return self.session.query(Transaction).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    def get_fraud_transactions(self, limit=100):
        """
        Get all fraudulent transactions
        
        Args:
            limit (int): Maximum number to return
            
        Returns:
            list: List of fraudulent transactions
        """
        return self.session.query(Transaction).filter_by(is_fraud=True).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    def update_transaction_prediction(self, transaction_id, prediction_result):
        """
        Update transaction with prediction results
        
        Args:
            transaction_id (int): Transaction ID
            prediction_result (dict): Prediction results
        """
        transaction = self.get_transaction(transaction_id)
        if transaction:
            transaction.is_fraud = prediction_result['is_fraud']
            transaction.fraud_probability = prediction_result['fraud_probability']
            transaction.risk_level = prediction_result['risk_level']
            transaction.updated_at = datetime.utcnow()
            self.session.commit()
    
    def add_prediction_log(self, log_data):
        """
        Add a prediction to the log
        
        Args:
            log_data (dict): Prediction log details
            
        Returns:
            PredictionLog: Created log entry
        """
        log = PredictionLog(**log_data)
        self.session.add(log)
        self.session.commit()
        return log
    
    def get_prediction_logs(self, limit=100):
        """
        Get recent prediction logs
        
        Args:
            limit (int): Maximum number to return
            
        Returns:
            list: List of PredictionLog objects
        """
        return self.session.query(PredictionLog).order_by(PredictionLog.prediction_time.desc()).limit(limit).all()
    
    def get_statistics(self):
        """
        Get database statistics
        
        Returns:
            dict: Statistics dictionary
        """
        total_transactions = self.session.query(Transaction).count()
        total_fraud = self.session.query(Transaction).filter_by(is_fraud=True).count()
        total_predictions = self.session.query(PredictionLog).count()
        
        stats = {
            'total_transactions': total_transactions,
            'total_fraud': total_fraud,
            'total_legitimate': total_transactions - total_fraud,
            'fraud_percentage': (total_fraud / total_transactions * 100) if total_transactions > 0 else 0,
            'total_predictions': total_predictions
        }
        
        return stats
    
    def close(self):
        """Close database session"""
        self.session.close()


if __name__ == "__main__":
    # Test database operations
    db_ops = DatabaseOperations()
    
    print("Testing database operations...")
    
    # Get statistics
    stats = db_ops.get_statistics()
    print("\nDatabase Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    db_ops.close()
    print("\nDatabase operations test completed!")
