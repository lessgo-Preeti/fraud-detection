# 🎓 Credit Card Fraud Detection System
## Academic Deep Learning Project

---

## 📊 Project Overview

A comprehensive **Credit Card Fraud Detection System** that integrates:
- ✅ **Deep Learning** (Multilayer Perceptron with Regularization)
- ✅ **Database Management** (PostgreSQL/SQLite)
- ✅ **Web Development** (Flask Dashboard)
- ✅ **Cloud Deployment Ready** (Heroku/AWS/Azure)

---

## 🎯 Problem Statement

Credit card fraud causes billions in losses annually. This system uses **Deep Learning** to detect fraudulent transactions in real-time by analyzing transaction patterns and features, providing instant risk assessment to prevent financial losses.

---

## 🧠 Deep Learning Architecture

### Model: Multilayer Perceptron (MLP)

**Architecture:**
```
Input Layer (30 features)
    ↓
Hidden Layer 1: 64 neurons + ReLU + Dropout(0.3) + L2 Regularization
    ↓
Hidden Layer 2: 32 neurons + ReLU + Dropout(0.3) + L2 Regularization
    ↓
Output Layer: 1 neuron + Sigmoid
```

**Training Details:**
- **Optimizer**: Adam (learning_rate=0.001)
- **Loss Function**: Binary Crossentropy
- **Regularization**: L2 (0.001) + Dropout (0.3)
- **Techniques**: Early Stopping, Learning Rate Reduction
- **Class Balancing**: Class weights for imbalanced data
- **Metrics**: Accuracy, Precision, Recall, AUC

**Undergraduate Concepts Covered:**
1. Multilayer Perceptrons (MLP)
2. Backpropagation and Gradient Descent
3. Optimization Algorithms (Adam, SGD, Momentum)
4. Regularization Techniques (L2, Dropout, Early Stopping)
5. Activation Functions (ReLU, Sigmoid)
6. Loss Functions (Binary Crossentropy)
7. Performance Metrics (Precision, Recall, AUC, F1-Score)

---

## 💾 Database Integration

### Schema Design

**Tables:**

1. **transactions** - Store credit card transactions
   - 30 PCA features (V1-V28)
   - Amount, Time
   - Prediction results (is_fraud, fraud_probability, risk_level)
   - Timestamps

2. **prediction_logs** - Audit trail of all predictions
   - Transaction ID reference
   - Prediction details
   - Model version
   - Timestamp

3. **users** - User authentication (future enhancement)
   - Username, email, password hash
   - Role-based access control

**Database Technology:**
- Development: SQLite (lightweight, no setup)
- Production: PostgreSQL (scalable, robust)
- ORM: SQLAlchemy (Python SQL toolkit)

**Operations:**
- CRUD operations for transactions
- Query filtering (fraud vs legitimate)
- Statistics aggregation
- Transaction history tracking

---

## 🌐 Web Development

### Flask Web Application

**Pages:**

1. **Home** (`/`)
   - Project overview
   - Feature highlights
   - Navigation to other pages

2. **Predict** (`/predict`)
   - Transaction input form
   - Random value generator for testing
   - Real-time prediction

3. **Result** (`/result`)
   - Fraud probability display
   - Risk level classification
   - Visual confidence indicator

4. **Dashboard** (`/dashboard`)
   - Statistics overview
   - Recent transactions table
   - Fraud rate metrics

**API Endpoints:**
- `POST /api/predict` - Make predictions via API
- `GET /api/stats` - Get system statistics
- `GET /api/transactions` - Retrieve transaction history
- `GET /health` - Health check endpoint

**Frontend:**
- Responsive CSS design
- Interactive forms
- Data visualization
- Mobile-friendly interface

---

## ☁️ Cloud Deployment

### Deployment Options

**1. Heroku (Recommended for Demo)**
```bash
heroku create fraud-detection-app
git push heroku main
```

**2. AWS EC2**
- Launch Ubuntu instance
- Install Python and dependencies
- Run with Gunicorn
- Configure security groups

**3. Azure App Service**
- Create Web App
- Deploy from GitHub
- Configure environment variables

**4. Docker Container**
```dockerfile
FROM python:3.9-slim
COPY . /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "web.app:app"]
```

**Production Features:**
- Gunicorn WSGI server
- Environment variable configuration
- PostgreSQL database
- Logging and monitoring
- HTTPS support

---

## 📁 Project Structure

```
Deep Learning -1/
│
├── 📂 data/                      # Dataset directory
│   ├── creditcard.csv           # Kaggle dataset (download separately)
│   └── README.md
│
├── 📂 models/                    # Trained models
│   ├── fraud_detection_model.h5 # Keras model (generated)
│   ├── scaler.pkl               # Feature scaler (generated)
│   ├── training_history.pkl     # Training metrics (generated)
│   └── visualizations/          # Plots (generated)
│
├── 📂 src/                       # Deep Learning code
│   ├── __init__.py
│   ├── data_preprocessing.py    # Data loading, cleaning, scaling
│   ├── model.py                 # Neural network architecture
│   ├── train.py                 # Training script
│   ├── evaluate.py              # Model evaluation
│   └── predict.py               # Prediction functions
│
├── 📂 database/                  # Database operations
│   ├── __init__.py
│   ├── db_setup.py              # Schema creation
│   └── db_operations.py         # CRUD operations
│
├── 📂 web/                       # Web application
│   ├── __init__.py
│   ├── app.py                   # Flask application
│   ├── templates/               # HTML templates
│   │   ├── index.html          # Home page
│   │   ├── predict.html        # Prediction form
│   │   ├── result.html         # Result display
│   │   ├── dashboard.html      # Statistics dashboard
│   │   └── error.html          # Error page
│   └── static/                  # CSS/JS files
│       └── style.css           # Stylesheet
│
├── 📄 config.py                  # Configuration settings
├── 📄 requirements.txt           # Python dependencies
├── 📄 README.md                  # Project documentation
├── 📄 GETTING_STARTED.md         # Setup instructions
├── 📄 .gitignore                 # Git ignore rules
├── 📄 .env.example               # Environment variables template
└── 📄 Procfile                   # Heroku deployment config
```

---

## 🚀 Usage Guide

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Download Dataset
- Kaggle: https://www.kaggle.com/mlg-ulb/creditcardfraud
- Place `creditcard.csv` in `data/` folder

### 3. Setup Database
```bash
python database/db_setup.py
```

### 4. Train Model
```bash
python src/train.py
```

### 5. Evaluate Model
```bash
python src/evaluate.py
```

### 6. Run Web App
```bash
python web/app.py
```

Visit: http://localhost:5000

---

## 📊 Dataset Information

**Source**: Kaggle Credit Card Fraud Detection Dataset

**Statistics:**
- **Total Transactions**: 284,807
- **Features**: 30 (V1-V28 PCA components + Time + Amount)
- **Target**: Binary (0 = Normal, 1 = Fraud)
- **Class Distribution**: 
  - Normal: 284,315 (99.83%)
  - Fraud: 492 (0.17%)
- **Size**: ~150 MB
- **Time Period**: 2 days of transactions

**Features:**
- `Time`: Seconds elapsed since first transaction
- `V1-V28`: PCA-transformed features (confidentiality)
- `Amount`: Transaction amount
- `Class`: 0 (legitimate) or 1 (fraudulent)

---

## 📈 Expected Results

**Performance Metrics:**
- Accuracy: ~99%+
- Precision: ~85-95%
- Recall: ~75-85%
- F1-Score: ~80-90%
- AUC-ROC: ~95-98%

**Training Time:**
- CPU: 10-20 minutes
- GPU: 2-5 minutes

---

## 🎯 Key Features

### Innovation & Depth

1. **End-to-End ML Pipeline**
   - Data preprocessing with class balancing
   - Feature scaling and normalization
   - Model training with regularization
   - Comprehensive evaluation

2. **Production-Ready Web Application**
   - User-friendly interface
   - Real-time predictions
   - Transaction history tracking
   - Statistics dashboard

3. **Database Integration**
   - Persistent storage
   - Query capabilities
   - Audit logging
   - Scalable design

4. **Cloud Deployment**
   - Docker containerization
   - Environment configuration
   - Scalable architecture
   - API for integration

### Academic Rigor

- Covers all undergraduate DL syllabus topics
- Implements best practices (regularization, validation)
- Demonstrates understanding of optimization algorithms
- Shows practical application of theory

---

## 🏆 Project Highlights

✅ **Practical Application**: Real-world fraud detection problem  
✅ **Innovation**: Integrated system (DL + DB + Web + Cloud)  
✅ **Depth**: Complete ML pipeline from data to deployment  
✅ **Multiple Technologies**: Python, TensorFlow, Flask, SQL  
✅ **Scalability**: Cloud-ready architecture  
✅ **Documentation**: Comprehensive guides and comments  
✅ **Best Practices**: Modular code, version control, testing  

---

## 📚 Technologies Used

**Deep Learning:**
- TensorFlow 2.15
- Keras
- NumPy
- Pandas
- Scikit-learn

**Database:**
- SQLAlchemy
- PostgreSQL / SQLite
- psycopg2

**Web Framework:**
- Flask
- Flask-CORS
- Jinja2 Templates
- HTML/CSS

**Deployment:**
- Gunicorn
- Docker
- Heroku/AWS/Azure

**Development:**
- Python 3.8+
- Git
- Virtual Environment

---

## 🔮 Future Enhancements

1. **Advanced ML**
   - Ensemble methods (Random Forest + MLP)
   - LSTM for temporal patterns
   - Autoencoder for anomaly detection

2. **Web Features**
   - User authentication
   - Batch CSV upload
   - Interactive visualizations (Plotly)
   - Email alerts for fraud

3. **Deployment**
   - Kubernetes orchestration
   - CI/CD pipeline
   - Monitoring (Prometheus/Grafana)
   - A/B testing framework

4. **Database**
   - Data warehouse integration
   - Historical analysis
   - Reporting dashboard
   - Export functionality

---

## 👨‍🎓 Learning Outcomes

By completing this project, you will:

✅ Understand end-to-end ML project development  
✅ Implement neural networks with regularization  
✅ Handle imbalanced datasets  
✅ Integrate ML with databases  
✅ Build web applications for ML models  
✅ Deploy ML systems to cloud  
✅ Follow software engineering best practices  

---

## 📞 Support & Resources

**Dataset:** https://www.kaggle.com/mlg-ulb/creditcardfraud  
**TensorFlow Docs:** https://www.tensorflow.org/  
**Flask Docs:** https://flask.palletsprojects.com/  
**SQLAlchemy Docs:** https://www.sqlalchemy.org/  

---

## 📄 License

This is an academic project for educational purposes.

---

## ✨ Conclusion

This project demonstrates a **complete, production-ready** credit card fraud detection system that integrates **Deep Learning, Database Management, Web Development, and Cloud Deployment**—perfect for an undergraduate Deep Learning course project that showcases both theoretical understanding and practical implementation skills.

**Ready to impress your professors and peers! 🚀**
