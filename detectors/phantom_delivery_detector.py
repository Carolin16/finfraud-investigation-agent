from interfaces.base_detector import AnomalyDetector
class PhantomDeliveryDetector(AnomalyDetector):

    def detect(self, invoice:dict)->dict:
        if invoice["gr_amount"] == 0:
            return {
                "anomaly_type": "phantom_delivery",
                "is_anomaly": True,
                "reason": "Phantom Delivery"
            }
        
        return {
            "anomaly_type": None,
            "is_anomaly": False
            }