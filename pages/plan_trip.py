import streamlit as st
from utils.auth import is_authenticated
import logging

logger = logging.getLogger(__name__)

# Sidebar exact same as app.py with style improvements to avoid stacking
with st.sidebar:
    # Sidebar title with custom style, replace with your exact app.py style if different
    st.markdown(
        """
        <style>
        .sidebar-title {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 20px;
            color: #1E88E5;
            font-family: 'Roboto', sans-serif;
        }
        .nav-button {
            width: 100%;
            margin: 5px 0;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.markdown('<div class="sidebar-title">🌍 Navigation</div>', unsafe_allow_html=True)

    if st.button("🏠 Home", key="nav_home"):
        st.query_params.clear()
        st.query_params.update({"path": "/"})
        st.experimental_rerun()

    if st.button("✈️ Plan Trip", key="nav_plan_trip"):
        st.experimental_set_query_params(path="/plan_trip")
        st.experimental_rerun()

    if "trip_data" in st.session_state:
        if st.button("📜 View Trip", key="nav_view_trip"):
            st.experimental_set_query_params(path="/view_trip")
            st.experimental_rerun()

    if is_authenticated():
        if st.button("🚪 Sign Out", key="sign_out"):
            st.session_state.clear()
            st.query_params.clear()
            st.experimental_rerun()


# The main page content...

def main():
    if not is_authenticated():
        st.error("Please sign in to plan your trip.")
        st.stop()

    st.title("Plan Your Trip")

    with st.form(key="trip_form"):
        destination = st.text_input("Enter Destination", "Mohenjo-Daro", help="Enter your travel destination.")
        days = st.slider("Number of Days", 1, 30, 1, help="Select the number of days for your trip.")
        budget = st.selectbox("Budget Level", ["Luxury", "Mid-range", "Budget"], help="Choose your budget.")
        traveler_type = st.selectbox("Traveler Type", ["Solo", "Couple", "Family", "Group"], help="Select traveler type.")

        submitted = st.form_submit_button("Generate Trip Plan")

        if submitted:
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
                st.success("Trip plan generated! Redirecting...")
                st.experimental_rerun()

if __name__ == "__main__":
    main()
