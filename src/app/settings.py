# src/app/settings.py
import streamlit as st
from src.services.user_service import UserService
from src.services.subscription_service import SubscriptionService

def main():
    st.title("⚙️ User Settings")

    # --- Ensure logged in ---
    if "user" not in st.session_state:
        st.warning("Please login first.")
        return

    user_service = UserService()
    sub_service = SubscriptionService()
    user = st.session_state["user"]

    # --- Show user info ---
    st.subheader("Your Info")
    st.write(f"👤 Name: {user['name']}")
    st.write(f"📧 Email: {user['email']}")
    st.write(f"📱 Phone: {user.get('phone', '-')}")

    # --- Fetch user_id from DB (ensure exists) ---
    user_data = user_service.get_user(user["email"])
    if not user_data.data:
        st.error("User not found in database")
        return
    user_id = user_data.data[0]["user_id"]

    # --- Manage subscriptions ---
    st.subheader("Your Subscriptions")
    subs = sub_service.get_subscriptions(user_id)
    if subs.data:
        for s in subs.data:
            status = "Active ✅" if s["active"] else "Inactive ❌"
            st.write(f"{s['alert_type']} — {status}")
            if s["active"]:
                if st.button(f"Unsubscribe {s['alert_type']}", key=f"unsub_{s['sub_id']}"):
                    sub_service.unsubscribe(s["sub_id"])
                    st.rerun()
    else:
        st.info("No subscriptions yet.")

    # --- Add new subscription ---
    st.subheader("Add New Subscription")
    new_alert_type = st.selectbox("Alert Type", ["Email", "SMS"])
    if st.button("Subscribe"):
        sub_service.subscribe(user_id, new_alert_type)
        st.success(f"Subscribed to {new_alert_type}!")
        st.rerun()
        # Show logout button if logged in
        # if "user" in st.session_state:
    if st.button("🚪 Logout"):
        st.session_state.pop("user")
        st.success("You have been logged out.")
        st.rerun()

