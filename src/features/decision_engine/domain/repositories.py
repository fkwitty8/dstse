from abc import ABC, abstractmethod
from typing import Dict

class BayesianNetworkRepository(ABC):
    @abstractmethod
    def query(self, evidence: Dict[str, str]) -> Dict[str, float]:
        """
        evidence: dict with keys 'Weather' and 'Traffic' and values as strings.
        Returns a dict mapping Decision states to probabilities.
        """
        pass
    
class SVMPolicyRepository(ABC):
    @abstractmethod
    def decide(self, delay_prob: float, importance: str) -> str:
        """Return final decision ('Scheduled', 'Online', 'Rescheduled', 'Cancelled')."""
        pass
