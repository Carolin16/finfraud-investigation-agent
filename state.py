
from typing import TypedDict,List,Optional

class AgentState(TypedDict):
    invoice: dict
    anomaly_flags: List[dict]
    ml_score : float
    risk_level : str
    decision : str
    similar_cases : List[str]
    sar_report : Optional[str]
    explanation : str
