class Thresholds:
    def __init__(self):
        self.limits = {
            "pm25": 25,
            "co2": 1000,
            "aqi": 100
        }

    def get(self, pollutant):
        return self.limits.get(pollutant.lower(), 9999)
