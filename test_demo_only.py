import sys
import os
sys.path.insert(0, '.')

# Hide model files temporarily
model_path = "models/fraud_detection_model.h5"
scaler_path = "models/scaler.pkl"
model_backup = None
scaler_backup = None

if os.path.exists(model_path):
    model_backup = model_path + ".test_hidden"
    os.rename(model_path, model_backup)
    print(f"Hidden: {model_path}")

if os.path.exists(scaler_path):
    scaler_backup = scaler_path + ".test_hidden"
    os.rename(scaler_path, scaler_backup)
    print(f"Hidden: {scaler_path}")

try:
    from web.app import get_predictor
    
    print("\nTesting get_predictor() in DEMO MODE...")
    p = get_predictor()
    print(f"Predictor type: {type(p)}")
    print(f"Demo mode: {p.is_demo_mode}")
    
    test = {f'V{i}': 0.5 for i in range(1,29)}
    test['Amount'] = 100
    test['Time'] = 3600
    
    r = p.predict_single(test)
    print(f"\n Prediction works: {r['is_fraud']}")
    print(f"Probability: {r['fraud_probability']:.4f}")
    print(f"Risk Level: {r['risk_level']}")
    print(f"Demo Mode in result: {r.get('demo_mode', False)}")
    print("\n✅ SUCCESS - Demo mode works perfectly!")
    
finally:
    # Restore files
    if model_backup and os.path.exists(model_backup):
        os.rename(model_backup, model_path)
        print(f"\nRestored: {model_path}")
    if scaler_backup and os.path.exists(scaler_backup):
        os.rename(scaler_backup, scaler_path)
        print(f"Restored: {scaler_path}")
