# Getting Started Guide

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Download Dataset

1. Visit Kaggle: https://www.kaggle.com/mlg-ulb/creditcardfraud
2. Download `creditcard.csv`
3. Create a `data` folder in the project root
4. Place `creditcard.csv` in the `data` folder

```bash
mkdir data
# Place creditcard.csv in the data folder
```

### Step 3: Setup Database

```bash
python database/db_setup.py
```

This will create a SQLite database file (`fraud_detection.db`) in the project root.

### Step 4: Train the Model

```bash
python src/train.py
```

This will:
- Load and preprocess the data
- Train the neural network
- Save the trained model to `models/fraud_detection_model.h5`
- Save the scaler to `models/scaler.pkl`
- Generate training visualizations

**Training time**: ~10-20 minutes on CPU, ~2-5 minutes on GPU

### Step 5: Evaluate the Model (Optional)

```bash
python src/evaluate.py
```

This generates:
- Confusion matrix
- ROC curve
- Precision-Recall curve
- Classification report

### Step 6: Run the Web Application

```bash
python web/app.py
```

The application will start on `http://localhost:5000`

Open your browser and navigate to:
- http://localhost:5000 - Home page
- http://localhost:5000/predict - Make predictions
- http://localhost:5000/dashboard - View statistics

## 🧪 Testing Without Training

If you want to test the web interface without training (for development):

1. Skip Step 4 (training)
2. The predict endpoint will show an error about missing model
3. You can still test the UI and database functionality

## 📊 Making Predictions

### Via Web Interface:
1. Go to http://localhost:5000/predict
2. Click "Generate Random Values" to populate the form
3. Click "Predict Fraud"

### Via API:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "V1": -1.359807134,
    "V2": -0.072781173,
    ...
    "Amount": 149.62,
    "Time": 0
  }'
```

## 🐳 Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "web/app.py"]
```

Build and run:
```bash
docker build -t fraud-detection .
docker run -p 5000:5000 fraud-detection
```

## ☁️ Cloud Deployment

### Heroku:

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Deploy
git push heroku main
```

### AWS/Azure:
- Upload to EC2/App Service
- Install dependencies
- Run with gunicorn: `gunicorn web.app:app`

## 🔧 Troubleshooting

### Issue: Dataset not found
**Solution**: Ensure `creditcard.csv` is in the `data/` folder

### Issue: Model not found
**Solution**: Run training first: `python src/train.py`

### Issue: Database error
**Solution**: Run database setup: `python database/db_setup.py`

### Issue: Port 5000 already in use
**Solution**: Change port in `config.py` or kill the process using port 5000

## 📝 Configuration

Edit `config.py` to customize:
- Model architecture (layers, neurons)
- Training parameters (epochs, batch size)
- Database settings
- Flask settings

## 🎓 Project Structure Explained

- `src/` - Deep Learning code (model, training, evaluation)
- `database/` - Database schema and operations
- `web/` - Flask web application
- `data/` - Dataset storage
- `models/` - Trained models and visualizations
- `config.py` - Central configuration
- `requirements.txt` - Python dependencies

## 💡 Tips

1. Use Google Colab if you don't have a GPU
2. Start with a small subset of data for quick testing
3. Monitor training progress with the visualizations
4. Check the dashboard to see prediction statistics

## 📚 Next Steps

1. ✅ Train model with different architectures
2. ✅ Implement user authentication
3. ✅ Add batch prediction from CSV upload
4. ✅ Create API documentation
5. ✅ Add monitoring and logging
6. ✅ Implement model versioning

Happy detecting! 🚀
