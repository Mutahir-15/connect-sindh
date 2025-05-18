
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
        st.rerun()

    if st.button("✈️ Plan Trip", key="nav_plan_trip"):
        st.experimental_set_query_params(path="/plan_trip")
        st.rerun()

    if "trip_data" in st.session_state:
        if st.button("📜 View Trip", key="nav_view_trip"):
            st.experimental_set_query_params(path="/view_trip")
            st.rerun()

    if is_authenticated():
        if st.button("🚪 Sign Out", key="sign_out"):
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()


# The main page content...

def main():
    if not is_authenticated():
        st.error("Please sign in to plan your trip.")
        st.stop()

    st.title("Plan Your Trip")

    # Initialize a flag to track if the form has been submitted
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    with st.form(key="trip_form"):
        destination = st.text_input("Enter Destination", "Mohenjo-Daro", help="Enter your travel destination.")
        days = st.slider("Number of Days", 1, 30, 1, help="Select the number of days for your trip.")
        budget = st.selectbox("Budget Level", ["Luxury", "Mid-range", "Budget"], help="Choose your budget.")
        traveler_type = st.selectbox("Traveler Type", ["Solo", "Couple", "Family", "Group"], help="Select traveler type.")

        submitted = st.form_submit_button("Generate Trip Plan")

        if submitted:
            if not destination.strip():
                st.error("Please enter a destination.")
            else:
                # Store trip data and set the submitted flag
                st.session_state.trip_data = {
                    "destination": destination,
                    "days": days,
                    "budget": budget,
                    "traveler_type": traveler_type
                }
                st.session_state.form_submitted = True
                logger.info(f"Trip data set: {st.session_state.trip_data}")
                st.success("Trip plan generated!")

    # Display the trip plan if the form has been submitted and trip data exists
    if st.session_state.form_submitted and "trip_data" in st.session_state:
        st.subheader("Your Trip Plan")
        trip_data = st.session_state.trip_data
        st.write(f"**Destination**: {trip_data['destination']}")
        st.write(f"**Number of Days**: {trip_data['days']}")
        st.write(f"**Budget Level**: {trip_data['budget']}")
        st.write(f"**Traveler Type**: {trip_data['traveler_type']}")
        # Optional: Button to view detailed plan in view_trip.py
        if st.button("View Detailed Plan"):
            st.switch_page("pages/view_trip.py")

        # Add hotel recommendations under the trip plan
        st.subheader("Recommended Hotels")

        # CSS for hotel cards with hover effect and clickable link
        st.markdown(
            """
            <style>
            .hotel-card {
                background-color: #424242;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                color: #E0E0E0;
                cursor: pointer;
            }
            .hotel-card:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            }
            .hotel-card:hover .maps-link {
                display: block;
            }
            .maps-link {
                display: none;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: #1E88E5;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                text-decoration: none;
                font-weight: 500;
            }
            .maps-link:hover {
                background-color: #1565C0;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Hotel data with Google Maps links
        hotels = [
            {"name": "Hotel One Karachi", "location": "Karachi, Sindh", "google_maps_link": "https://maps.google.com/?q=Hotel+One+Karachi"},
            {"name": "Serena Hotel Thatta", "location": "Thatta, Sindh", "google_maps_link": "https://maps.google.com/?q=Serena+Hotel+Thatta"},
            # Add more hotels as needed
        ]
        for hotel in hotels:
            st.markdown(
                f"""
                <a href="{hotel['google_maps_link']}" target="_blank" style="text-decoration: none;">
                    <div class="hotel-card">
                        <h3>{hotel['name']}</h3>
                        <p>{hotel['location']}</p>
                        <span class="maps-link">View on Google Maps</span>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()