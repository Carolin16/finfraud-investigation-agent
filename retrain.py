import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv('data/p2p_invoices.csv')
FEATURES = ['po_amount', 'invoice_amount', 'gr_amount', 'deviation_pct', 'days_since_last_invoice', 'is_new_vendor', 'three_way_match']
X = df[FEATURES]
y = df['label']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
joblib.dump(model, 'models/random_forest.joblib')
print('Model saved')