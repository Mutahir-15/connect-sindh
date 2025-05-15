import streamlit as st
from utils.auth import is_authenticated
import logging

logger = logging.getLogger(__name__)

# Sidebar navigation
with st.sidebar:
        st.markdown('<div class="sidebar-title">🌍 Navigation</div>', unsafe_allow_html=True)

        if st.button("🏠 Home", key="nav_home"):
            st.query_params.clear()
            st.query_params.update({"path": "/"})
            st.rerun()

        if st.button("✈️ Plan Trip", key="nav_plan_trip"):
            st.switch_page("pages/plan_trip.py")

        if "trip_data" in st.session_state:
            if st.button("📜 View Trip", key="nav_view_trip"):
                st.switch_page("pages/view_trip.py")

        if is_authenticated():
            if st.button("🚪 Sign Out", key="sign_out"):
                st.session_state.clear()
                st.query_params.clear()
                st.rerun()

# The logic here will check whether the User is logged in or not.
def main():
    if not is_authenticated():
        st.error("Please sign in to plan your trip.")
        st.stop()

# This is the card where the User will put the data on which the plan will be generated
    st.header("Plan Your Trip")
    with st.form(key="trip_form"):
        destination = st.text_input("Enter Destination", "Mohenjo-Daro", help="Enter your travel destination.")
        days = st.slider("Number of Days", 1, 30, 1, help="Select the number of days.")
        budget = st.selectbox("Budget Level", ["Luxury", "Mid-range", "Budget"], help="Choose your budget.")
        traveler_type = st.selectbox("Traveler Type", ["Solo", "Couple", "Family", "Group"], help="Select traveler type.")
        if st.form_submit_button("Generate Trip Plan"):
            if not destination.strip():
                st.error("Please enter a valid destination.")
            else:
                st.session_state.trip_data = {
                    "destination": destination,
                    "days": days,
                    "budget": budget,
                    "traveler_type": traveler_type
                }
                logger.info(f"Trip data set: {st.session_state.trip_data}")
                st.switch_page("pages/view_trip.py")

if __name__ == "__main__":
    main()
