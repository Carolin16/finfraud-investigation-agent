import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,roc_auc_score
import joblib

"""
classification_report, roc_auc_score - tells you how well the model performs
joblib — saves the trained model to a file
"""

df = pd.read_csv("data/p2p_invoices.csv")


FEATURES = [
    "po_amount", "invoice_amount", "gr_amount",
    "deviation_pct", "days_since_last_invoice",
    "is_new_vendor", "three_way_match"
]

X = df[FEATURES]
y = df["label"]

X_train ,  X_test , y_train , y_test = train_test_split(X , y, test_size=0.2,random_state=42)
"""
- n_estimators=100 — builds 100 decision trees and combines them - forest
- random_state=42 — keeps results consistent each run
- .fit() — where the actual learning happens
"""
model = RandomForestClassifier(n_estimators=100,random_state=42)
model.fit(X_train,y_train)

"""
predict_proba() returns a 2-column array — one column per class
[[0.85, 0.15]]   ← 85% chance normal, 15% chance anomaly
"""
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[: ,-1]

joblib.dump(model,"models/random_forest.joblib")
