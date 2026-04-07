from typing import Dict
from ...domain.entities import Lecture, WeatherPrediction, TrafficPrediction, LectureDecision
from ...domain.repositories import BayesianNetworkRepository, SVMPolicyRepository
from ...infrastructure.clients.weather_client import WeatherAPIClient
from ...infrastructure.clients.traffic_client import TrafficAPIClient

class PredictLectureStatusUseCase:
    def __init__(self,
                 weather_client: WeatherAPIClient,
                 traffic_client: TrafficAPIClient,
                 bn_service: BayesianNetworkRepository,
                 svm_service: SVMPolicyRepository):
        self.weather_client = weather_client
        self.traffic_client = traffic_client
        self.bn_service = bn_service
        self.svm_service = svm_service

    def execute(self, lecture: Lecture) -> LectureDecision:
        # 1. Get weather prediction
        weather_res = self.weather_client.predict(
            lecture.datetime,
            lecture.dry_bulb,
            lecture.wet_bulb,
            lecture.humidity,
            lecture.wind_speed
        )

        # 2. Get traffic prediction
        traffic_res = self.traffic_client.predict(lecture.datetime, lecture.road_name)

        # 3. Query BN with weather and traffic categories
        evidence = {
            'Weather': weather_res['bn_category'],
            'Traffic': traffic_res['congestion']
        }
        decision_probs = self.bn_service.query(evidence)

        # 4. Compute delay probability (e.g., sum of disruptive states)
        delay_prob = sum(decision_probs.get(state, 0) for state in ['Online', 'Rescheduled', 'Cancelled'])

        # 5. Apply SVM policy
        final_decision = self.svm_service.decide(delay_prob, lecture.importance)

        # 6. Build explanation
        explanation = (f"Weather: {weather_res['bn_category']} (conf={weather_res['confidence']:.2f}), "
                       f"Traffic: {traffic_res['congestion']} (conf={traffic_res['confidence']:.2f}), "
                       f"Delay prob: {delay_prob:.2f}, Importance: {lecture.importance}")

        return LectureDecision(
            decision=final_decision,
            probabilities=decision_probs,
            delay_probs=delay_prob,   # optional
            explanation=explanation
        )