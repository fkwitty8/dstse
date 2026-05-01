import joblib
import os
#local host mode
# from ..domain.repositories import SVMPolicyRepository

# dockermode
from features.decision_engine.domain.repositories import SVMPolicyRepository

class TrainedSVMPolicy(SVMPolicyRepository):
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self._load()

    def _load(self):
        self.model = joblib.load(os.path.join(self.model_dir, "svm_policy_model.pkl"))
        self.le_imp = joblib.load(os.path.join(self.model_dir, "importance_map.pkl"))
        self.le_dec = joblib.load(os.path.join(self.model_dir, "decision_encoder.pkl"))

    def decide(self, delay_prob: float, importance: str) -> str:
        imp_val = self.le_imp[importance]
        pred_enc = self.model.predict([[delay_prob, imp_val]])[0]
        return self.le_dec.inverse_transform([pred_enc])[0]