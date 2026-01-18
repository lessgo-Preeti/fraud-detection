# Quick Reference Card 📋

## Installation
```bash
pip install -r requirements.txt
```

## Setup
```bash
# 1. Download dataset
# Visit: https://www.kaggle.com/mlg-ulb/creditcardfraud
# Place creditcard.csv in data/

# 2. Setup database
python database/db_setup.py

# 3. Train model (~10-20 min)
python src/train.py

# 4. Evaluate (optional)
python src/evaluate.py

# 5. Run web app
python web/app.py
```

## URLs
- **Home**: http://localhost:5000
- **Predict**: http://localhost:5000/predict
- **Dashboard**: http://localhost:5000/dashboard
- **API**: http://localhost:5000/api/predict

## API Example
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "V1": -1.35, "V2": -0.07, ..., "Amount": 149.62, "Time": 0
  }'
```

## File Locations
- **Dataset**: `data/creditcard.csv`
- **Model**: `models/fraud_detection_model.h5`
- **Scaler**: `models/scaler.pkl`
- **Database**: `fraud_detection.db`
- **Config**: `config.py`

## Model Architecture
```
Input (30) → Dense(64,ReLU) → Dropout(0.3) 
          → Dense(32,ReLU) → Dropout(0.3) 
          → Dense(1,Sigmoid)
```

## Common Issues

**Dataset not found**
```bash
# Download from Kaggle and place in data/
mkdir data
# copy creditcard.csv to data/
```

**Model not found**
```bash
# Train the model first
python src/train.py
```

**Port already in use**
```bash
# Change port in config.py
FLASK_PORT = 5001
```

## Project Components
- ✅ Deep Learning (MLP + Regularization)
- ✅ Database (SQLite/PostgreSQL)
- ✅ Web App (Flask + HTML/CSS)
- ✅ API (RESTful endpoints)
- ✅ Cloud Ready (Heroku/AWS/Azure)

## Key Metrics
- Accuracy: ~99%+
- Precision: ~85-95%
- Recall: ~75-85%
- AUC: ~95-98%

## Deployment

### Heroku
```bash
heroku create app-name
git push heroku main
```

### Docker
```bash
docker build -t fraud-detection .
docker run -p 5000:5000 fraud-detection
```

## Configuration
Edit `config.py` for:
- Model architecture
- Training parameters
- Database settings
- Flask configuration

## Technologies
- TensorFlow/Keras
- Flask
- SQLAlchemy
- PostgreSQL/SQLite
- Pandas/NumPy
- Scikit-learn

## Need Help?
- Check `GETTING_STARTED.md`
- Read `PROJECT_DOCUMENTATION.md`
- Review code comments
