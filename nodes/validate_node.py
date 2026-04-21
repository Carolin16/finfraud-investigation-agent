from state import AgentState
from validators.invoice_validator import InvoiceValidator

def validate_invoice(state : AgentState) -> AgentState:
    validator = InvoiceValidator()
    try:
        validator.validate(state["invoice"])
        state["decision"] = "valid"
    except ValueError as e:
        state["decision"] = "invalid"
        state["explanation"] = str(e)
    return state
