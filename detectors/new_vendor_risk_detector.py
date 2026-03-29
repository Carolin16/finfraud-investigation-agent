from interfaces.base_detector import AnomalyDetector
class NewVendorRiskDetector(AnomalyDetector):

    def detect(self, invoice:dict):
        if invoice["is_new_vendor"] and invoice["invoice_amount"] > 10000:
            return {
                "anomaly_type": "new_vendor_risk",
                "is_anomaly": True,
                "reason": "New Vendor Risk"
            }
        
        return {
            "anomaly_type": None,
            "is_anomaly": False
            }