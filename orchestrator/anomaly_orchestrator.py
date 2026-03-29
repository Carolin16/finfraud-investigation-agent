from interfaces.base_detector import AnomalyDetector
class AnomalyOrchestrator:
    def __init__(self,detectors : list[AnomalyDetector]):
        self.detectors = detectors

    def run(self, invoice:dict) -> list[dict]:
        results = []

        
        for detector in self.detectors:
            result = detector.detect(invoice)

            if result["is_anomaly"]:
                results.append(result)

        return results
