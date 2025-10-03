from src.dao.alert_dao import AlertDAO
from src.dao.threshold_dao import ThresholdDAO

class AlertService:
    def __init__(self):
        self.alert_dao = AlertDAO()
        self.threshold_dao = ThresholdDAO()

    def check_and_trigger_alert(self, pollutant, value, user_id, data_id=None):
        threshold = self.threshold_dao.get_by_pollutant(pollutant)
        limit = threshold.data["max_value"] if threshold.data else None
        if limit and value > limit:
            self.alert_dao.insert("Email", user_id, data_id, threshold.data["threshold_id"])
            return f"⚠️ {pollutant} exceeded safe limit {limit} with value {value}"
        return None

