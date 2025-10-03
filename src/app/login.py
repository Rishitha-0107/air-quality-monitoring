# src/app/login.py
import streamlit as st
from src.services.user_service import UserService

def login_page():
    st.title("🌍 Air Quality Monitoring - Login")

    user_service = UserService()

    # --- Login Section ---
    email = st.text_input("Enter your Email")

    if st.button("Login"):
        if not email:
            st.error("Please enter your email")
        else:
            result = user_service.get_user(email)
            if result.data:  # user exists
                user = result.data[0]
                # ✅ Store only minimal info
                st.session_state["user"] = {
                    "user_id": user["user_id"],
                    "name": user.get("name", "Guest"),
                    "email": user["email"],
                    "phone": user.get("phone", "")
                }
                st.success(f"Welcome back, {st.session_state['user']['name']}!")
                st.rerun()
            else:
                st.warning("No account found. Please register below.")

    # --- Registration Section ---
    st.subheader("🆕 New User? Register Here")
    with st.form("register_form"):
        name = st.text_input("Name")
        reg_email = st.text_input("Email (for registration)")
        phone = st.text_input("Phone Number")
        submitted = st.form_submit_button("Register")

        if submitted:
            if not name or not reg_email:
                st.error("Name and Email are required!")
            else:
                result = user_service.register_user(name, reg_email, phone)
                if result.data:
                    user = result.data[0]
                    # ✅ Again store only minimal info
                    st.session_state["user"] = {
                        "user_id": user["user_id"],
                        "name": user.get("name", name),
                        "email": user["email"],
                        "phone": user.get("phone", phone)
                    }
                    st.success(f"Registered successfully! Welcome, {st.session_state['user']['name']}.")
                    st.rerun()
                else:
                    st.error("Registration failed. Please try again.")
