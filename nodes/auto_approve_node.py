from state import AgentState

def auto_approve(state : AgentState) -> AgentState:
    state["decision"] = "auto_approved"
    state["explanation"] = (
        f"Invoice cleared. Ml fraud score : {state['ml_score']:.2f} "
        f"(below threshold). No anomaly flags raised."
    )
    return state
