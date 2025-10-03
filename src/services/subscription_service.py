from src.dao.subscription_dao import SubscriptionDAO

class SubscriptionService:
    def __init__(self):
        self.dao = SubscriptionDAO()

    def subscribe(self, user_id, alert_type):
        return self.dao.add_subscription(user_id, alert_type)

    def get_subscriptions(self, user_id):
        return self.dao.get_by_user(user_id)

    def unsubscribe(self, sub_id):
        return self.dao.deactivate(sub_id)
