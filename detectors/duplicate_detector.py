from interfaces.base_detector import AnomalyDetector
class DuplicateDetector(AnomalyDetector):
    """
     Data is synthetically generated 
     For simplification labelled invoices with low days as duplicates
     anomaly_type == "duplicate" → their days ranged from 1 to 7
     anomaly_type == "none" → their days ranged from 11 to 53
    """

    def detect(self, invoice:dict) ->dict:
        if invoice["days_since_last_invoice"] <= 7:
            return {
                "anomaly_type": "duplicate_invoice",
                "is_anomaly": True,
                "reason": "Duplicate billing of invoice"
            }
        
        return {
            "anomaly_type": None,
            "is_anomaly": False
            }