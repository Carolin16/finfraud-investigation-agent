from state import AgentState

def flag_for_review(state : AgentState) -> AgentState:
    # for medium risk (0.4 -0.7)
    state["decision"] = "flagged_for_human_review"
    
    flag_names = [f["anomaly_type"] for f in state["anomaly_flags"]]
    flags_str = ", ".join(flag_names) if flag_names else "none"

    state["explanation"] = (

        f"Invoice flagged for human review. Ml fraud score : {state['ml_score']:.2f}"
        f"Anomalies detected ; {flags_str}. "
        f"Queued for analyst inspection."
    )
    return state

