"""
Database setup script for Credit Card Fraud Detection System
Creates necessary tables and schema
"""

from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

Base = declarative_base()


class Transaction(Base):
    """
    Transaction table to store credit card transactions
    """
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    
    # PCA features V1-V28
    v1 = Column(Float)
    v2 = Column(Float)
    v3 = Column(Float)
    v4 = Column(Float)
    v5 = Column(Float)
    v6 = Column(Float)
    v7 = Column(Float)
    v8 = Column(Float)
    v9 = Column(Float)
    v10 = Column(Float)
    v11 = Column(Float)
    v12 = Column(Float)
    v13 = Column(Float)
    v14 = Column(Float)
    v15 = Column(Float)
    v16 = Column(Float)
    v17 = Column(Float)
    v18 = Column(Float)
    v19 = Column(Float)
    v20 = Column(Float)
    v21 = Column(Float)
    v22 = Column(Float)
    v23 = Column(Float)
    v24 = Column(Float)
    v25 = Column(Float)
    v26 = Column(Float)
    v27 = Column(Float)
    v28 = Column(Float)
    
    # Prediction results
    is_fraud = Column(Boolean, nullable=True)
    fraud_probability = Column(Float, nullable=True)
    risk_level = Column(String(20), nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, is_fraud={self.is_fraud})>"


class PredictionLog(Base):
    """
    Log table to track all predictions made by the system
    """
    __tablename__ = 'prediction_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(Integer, nullable=True)
    is_fraud = Column(Boolean, nullable=False)
    fraud_probability = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    prediction_time = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String(50), nullable=True)
    
    def __repr__(self):
        return f"<PredictionLog(id={self.id}, is_fraud={self.is_fraud}, probability={self.fraud_probability})>"


class User(Base):
    """
    User table for authentication (future enhancement)
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user')  # user, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"


def create_database():
    """
    Create database and all tables
    """
    config = Config()
    
    print("="*70)
    print(" DATABASE SETUP")
    print("="*70)
    
    # Create engine
    print(f"\nCreating database connection...")
    print(f"Database type: {config.DB_TYPE}")
    print(f"Database URI: {config.DATABASE_URI}")
    
    # For SQLite, ensure directory exists
    if config.DB_TYPE == 'sqlite':
        db_dir = os.path.dirname(config.SQLITE_DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            print(f"Created directory: {db_dir}")
    
    engine = create_engine(config.DATABASE_URI, echo=False)  # Turn off echo for cleaner logs
    
    # Create all tables - this is idempotent (safe to call multiple times)
    print("\nCreating tables...")
    Base.metadata.create_all(engine, checkfirst=True)
    
    print("\n" + "="*70)
    print("DATABASE SETUP COMPLETED!")
    print("="*70)
    print("\nTables created:")
    print("1. transactions - Store credit card transactions")
    print("2. prediction_logs - Log all predictions")
    print("3. users - User authentication (future)")
    
    # Verify tables were created
    from sqlalchemy import inspect
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    print(f"\nVerified tables in database: {table_names}")
    
    return engine


def get_session():
    """
    Create a database session
    
    Returns:
        Session: SQLAlchemy session object
    """
    config = Config()
    engine = create_engine(config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Setup database
    engine = create_database()
    
    # Test connection
    print("\nTesting database connection...")
    session = get_session()
    print("Database connection successful!")
    session.close()
