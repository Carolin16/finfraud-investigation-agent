from abc import ABC,abstractmethod

class AnomalyDetector(ABC):

    @abstractmethod
    def detect(self,invoice:dict) -> dict:
        pass