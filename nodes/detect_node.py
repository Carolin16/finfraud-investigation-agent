from state import AgentState
from orchestrator.anomaly_orchestrator import AnomalyOrchestrator
from detectors.duplicate_detector import DuplicateDetector
from detectors.phantom_delivery_detector import PhantomDeliveryDetector
from detectors.new_vendor_risk_detector import NewVendorRiskDetector
from detectors.overbilling_detector import OverbillingDetector

def detect_anomalies(state : AgentState) -> AgentState:

    # create an anomaly orchestrator
    orchestrator = AnomalyOrchestrator(detectors=[
        OverbillingDetector(),
        DuplicateDetector(),
        PhantomDeliveryDetector(),
        NewVendorRiskDetector()
    ])

    flags = orchestrator.run(state["invoice"])
    state["anomaly_flags"] = flags
    return state