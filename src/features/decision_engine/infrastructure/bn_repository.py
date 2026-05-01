import os
import pickle
import json
from pgmpy.inference import VariableElimination
from typing import Dict
# local host mode
# from ..domain.repositories import BayesianNetworkRepository

# docker mode
from features.decision_engine.domain.repositories import BayesianNetworkRepository

class FileBasedBNRepository(BayesianNetworkRepository):
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self._load_model()

    def _load_model(self):
        with open(os.path.join(self.model_dir, "bn_model.pkl"), 'rb') as f:
            self.model = pickle.load(f)
        print("loaded BN model from:", os.path.join(self.model_dir, "bn_model.pkl"))
        self.inference = VariableElimination(self.model)
        
        print("loading states")
        with open(os.path.join(self.model_dir, "states.json"), 'r') as f:
            self.states = json.load(f)
            
        print("loading evidence vars")
        with open(os.path.join(self.model_dir, "evidence_vars.json"), 'r') as f:
            self.evidence_vars = json.load(f)

    def query(self, evidence: Dict[str, str]) -> Dict[str, float]:
        # Evidence is already in state names (strings). 
        # we Pass them directly.
        result = self.inference.query(variables=['Decision'], evidence=evidence)
        decision_probs = {self.states['Decision'][i]: result.values[i] for i in range(4)}
        return decision_probs