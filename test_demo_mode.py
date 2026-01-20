"""Test demo mode functionality"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import FraudPredictor

# Test 1: With model file (if exists)
print("="*60)
print("TEST 1: Normal mode (with model)")
print("="*60)
try:
    predictor = FraudPredictor()
    predictor.load_model_and_scaler()
    print(f"✓ Demo Mode: {predictor.is_demo_mode}")
    
    test_data = {f'V{i}': 0.5 for i in range(1, 29)}
    test_data['Amount'] = 100.0
    test_data['Time'] = 3600.0
    
    result = predictor.predict_single(test_data)
    print(f"✓ Prediction: {result['is_fraud']}")
    print(f"✓ Probability: {result['fraud_probability']:.4f}")
    print(f"✓ Demo Mode in result: {result.get('demo_mode', False)}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Simulate missing model
print("\n" + "="*60)
print("TEST 2: Demo mode (simulating missing model)")
print("="*60)

# Temporarily rename model if it exists
model_path = "models/fraud_detection_model.h5"
backup_path = "models/fraud_detection_model.h5.backup_test"
model_existed = False

if os.path.exists(model_path):
    os.rename(model_path, backup_path)
    model_existed = True
    print("✓ Temporarily hid model file")

try:
    predictor2 = FraudPredictor()
    predictor2.load_model_and_scaler()
    print(f"✓ Demo Mode: {predictor2.is_demo_mode}")
    
    test_data2 = {f'V{i}': 0.5 for i in range(1, 29)}
    test_data2['Amount'] = 100.0
    test_data2['Time'] = 3600.0
    
    result2 = predictor2.predict_single(test_data2)
    print(f"✓ Prediction: {result2['is_fraud']}")
    print(f"✓ Probability: {result2['fraud_probability']:.4f}")
    print(f"✓ Demo Mode in result: {result2.get('demo_mode', True)}")
    print(f"✓ Risk Level: {result2['risk_level']}")
except Exception as e:
    print(f"✗ Error: {e}")
finally:
    # Restore model if it existed
    if model_existed and os.path.exists(backup_path):
        os.rename(backup_path, model_path)
        print("✓ Restored model file")

print("\n" + "="*60)
print("ALL TESTS COMPLETED!")
print("="*60)
