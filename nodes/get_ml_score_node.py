import joblib
from state import AgentState

# Exact same order as train.py
FEATURES = [
    "po_amount", "invoice_amount", "gr_amount",
    "deviation_pct", "days_since_last_invoice",
    "is_new_vendor", "three_way_match"
]

def get_ml_score(state : AgentState) -> AgentState:

    # Load the saved Random Forest model from disk
    model = joblib.load("models/random_forest.joblib")

    #Retrieve from state
    """
        invoice = {
            "po_amount": 10000,
            "invoice_amount": 15000,
            "gr_amount": 0,
            ...
        }
    """
    invoice = state["invoice"]

    #retrieve feature values from invoice state
    feature_values = [invoice[feature] for feature in FEATURES]

    """
        Wrap in 2D list (predict_proba needs a list of rows)
        predict_proba returns [[P(legit), P(fraud)]]
        We grab index [0][1] → the fraud probability
    """
    ml_score = model.predict_proba([feature_values])[0][1]
    state["ml_score"] = ml_score

    return state