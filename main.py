from detectors.duplicate_detector import DuplicateDetector
from detectors.new_vendor_risk_detector import NewVendorRiskDetector
from detectors.overbilling_detector import OverbillingDetector
from detectors.phantom_delivery_detector import PhantomDeliveryDetector
from orchestrator.anomaly_orchestrator import AnomalyOrchestrator

detectors = [DuplicateDetector(),NewVendorRiskDetector(),OverbillingDetector(),PhantomDeliveryDetector()]
orchestrator = AnomalyOrchestrator(detectors)

#sample 
invoice = {
    "invoice_id": "INV001",
    "vendor_id": "V123",
    "vendor_name": "Acme Corp",
    "vendor_category": "IT",
    "po_reference": "PO456",
    "po_amount": 1000,
    "invoice_amount": 3000000,   # make this > 1000 to trigger overbilling
    "gr_amount": 0,
    "deviation_pct": 0.30,
    "days_since_last_invoice": 4,
    "is_new_vendor": 1,
    "three_way_match": 0,
    "invoice_date": "2024-01-01",
    "anomaly_type": "overbilling",
    "label": 1
}

results = orchestrator.run(invoice)
print(results)