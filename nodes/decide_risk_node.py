from state import AgentState

HIGH_THRESHOLD = 0.7
MEDIUM_THRESHOLD = 0.2

# Anomaly types serious enough to force HIGH
# even if ml_score is only medium
# new vendor risk and overbilling are not categorized as high risk 
HIGH_RISK_ANOMALY_TYPES = {"phantom_delivery" , "duplicate"}

def decide_risk_node(state : AgentState) -> AgentState:

    # retrieve the state
    ml_score = state["ml_score"]
    anomaly_flags = state["anomaly_flags"]
    print(f"DEBUG: ml_score={ml_score}, MEDIUM_THRESHOLD={MEDIUM_THRESHOLD}, HIGH_THRESHOLD={HIGH_THRESHOLD}")
    # Collect the anomaly types detected
    # e.g. ["overbilling", "phantom_delivery"]
    detected_types = {flag["anomaly_type"] for flag in anomaly_flags}

    # Check if any serious anomaly types were found
    has_serious_anomaly = bool(detected_types & HIGH_RISK_ANOMALY_TYPES)

    if ml_score >= HIGH_THRESHOLD or has_serious_anomaly:
        risk_level = "HIGH"

    elif ml_score >= MEDIUM_THRESHOLD:
        risk_level = "MEDIUM"
    
    else:
        risk_level = "LOW"
    
    # update risk level state
    state["risk_level"] = risk_level

    return state
    
