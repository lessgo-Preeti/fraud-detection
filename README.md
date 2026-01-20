<<<<<<< HEAD
# Credit Card Fraud Detection System

## Project Overview
A comprehensive Deep Learning system to detect fraudulent credit card transactions using MLP neural networks, integrated with database management, web interface, and cloud deployment capabilities.

## Features
- **Deep Learning**: Multilayer Perceptron (MLP) with regularization
- **Database**: PostgreSQL for transaction storage and logging
- **Web Interface**: Flask-based dashboard for real-time detection
- **Cloud Ready**: Deployable on Heroku/AWS/Azure

## Project Structure
```
Deep Learning -1/
├── data/                      # Dataset directory
├── models/                    # Trained models
├── src/
│   ├── data_preprocessing.py  # Data loading and preprocessing
│   ├── model.py              # Neural network architecture
│   ├── train.py              # Training script
│   ├── evaluate.py           # Model evaluation
│   └── predict.py            # Prediction functions
├── database/
│   ├── db_setup.py           # Database schema
│   └── db_operations.py      # CRUD operations
├── web/
│   ├── app.py                # Flask application
│   ├── templates/            # HTML templates
│   └── static/               # CSS, JS files
├── requirements.txt          # Dependencies
└── config.py                 # Configuration settings
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Dataset
- Visit: https://www.kaggle.com/mlg-ulb/creditcardfraud
- Download creditcard.csv
- Place in `data/` folder

### 3. Setup Database
```bash
python database/db_setup.py
```

### 4. Train Model
```bash
python src/train.py
```

### 5. Run Web Application
```bash
python web/app.py
```

## Technologies Used
- **Deep Learning**: TensorFlow/Keras
- **Database**: PostgreSQL (SQLite for local)
- **Web Framework**: Flask
- **Deployment**: Docker, Heroku/AWS ready
- **Visualization**: Matplotlib, Seaborn

## Model Architecture
- Input Layer: 30 features
- Hidden Layer 1: 64 neurons (ReLU + Dropout 0.3)
- Hidden Layer 2: 32 neurons (ReLU + Dropout 0.3)
- Output Layer: 1 neuron (Sigmoid)
- Optimizer: Adam
- Loss: Binary Crossentropy
- Regularization: L2 + Dropout

## Dataset Information
- **Source**: Kaggle Credit Card Fraud Detection
- **Instances**: 284,807 transactions
- **Features**: 30 (V1-V28 PCA components + Time + Amount)
- **Class**: 0 (Normal), 1 (Fraud)
- **Imbalance**: 0.172% fraud cases

## Author
Deep Learning Project - Undergraduate Course
=======
# Fraud-Detection-System
>>>>>>> becc8a1655c60cdc71f4f40a8eb8966ce80944de
