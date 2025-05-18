import streamlit as st
from utils.auth import is_authenticated
from utils.api import generate_trip_plan, get_hotels
import logging

logger = logging.getLogger(__name__)

# Custom CSS applied for styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    .stApp {
        background: linear-gradient(to bottom, #212121, #303030);
        font-family: 'Roboto', sans-serif;
        color: #E0E0E0;
    }
    h2, h3 {
        color: #81C784;
        font-weight: 500;
    }
    .card {
        background-color: #424242;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.2s ease-in-out;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        st.error("Please sign in to view your trip.")
        st.stop()

# Will check the user has fulfilled the requirements on Planning a trip.
    if "trip_data" not in st.session_state:
        st.error("No trip data available. Please plan a trip first.")
        st.stop()

# Here the users provided information will be given to AI and the response will be generated accordingly.
    trip_data = st.session_state.trip_data
    logger.info(f"Rendering trip for: {trip_data}")
    with st.spinner("Generating your trip plan..."):
        itinerary = generate_trip_plan(trip_data["destination"], trip_data["days"], trip_data["budget"], trip_data["traveler_type"])
        hotels = get_hotels(trip_data["destination"])

# Generated plan using Gemini will be showed here.
    st.subheader("🗺️ Generated Itinerary")
    st.markdown(f'<div class="card">{itinerary}</div>', unsafe_allow_html=True)

    st.subheader("🏨 Recommended Hotels")
    for hotel in hotels:
        # Generate Google Maps search URL
        maps_query = f"{hotel['name']} {hotel['formatted_address']}".replace(' ', '+')
        maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"

        st.markdown(
            f"""
            <div class="card">
                <strong>🏨 {hotel['name']}</strong><br>
                Rating: {hotel.get('rating', 'N/A')} ⭐<br>
                📍 Address: {hotel['formatted_address']}<br>
                🔗 <a href="{maps_url}" target="_blank" style="color:#81C784;">View on Google Maps</a>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()