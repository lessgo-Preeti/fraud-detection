import sys
sys.path.insert(0, '.')

from web.app import get_predictor

print("Testing get_predictor()...")
p = get_predictor()
print(f"Predictor type: {type(p)}")
print(f"Demo mode: {p.is_demo_mode}")

test = {f'V{i}': 0.5 for i in range(1,29)}
test['Amount'] = 100
test['Time'] = 3600

r = p.predict_single(test)
print(f"Prediction works: {r['is_fraud']}")
print(f"Full result: {r}")
print("\n✅ SUCCESS - Predictor works!")
