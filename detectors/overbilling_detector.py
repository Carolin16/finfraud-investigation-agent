from interfaces.base_detector import AnomalyDetector

class OverbillingDetector(AnomalyDetector):

    
    def detect(self, invoice:dict) -> dict:
        if invoice["invoice_amount"] > invoice["po_amount"]:
            return {
                "anomaly_type": "overbilling",
                "is_anomaly": True,
                "reason": "Invoice amount exceeds PO amount"
            }
        
        return {
            "anomaly_type": None,
            "is_anomaly": False
            }