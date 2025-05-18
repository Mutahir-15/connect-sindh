
import streamlit as st
from utils.auth import is_authenticated

# Sidebar exact same as app.py and plan_trip.py with style improvements
with st.sidebar:
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

# Main page content
def main():
    if not is_authenticated():
        st.error("Please sign in to view your trip.")
        st.stop()

    st.title("Detailed Trip Plan")

    # Display the detailed trip plan
    if "trip_data" in st.session_state:
        trip_data = st.session_state.trip_data
        st.subheader("Trip Details")
        st.write(f"**Destination**: {trip_data['destination']}")
        st.write(f"**Duration**: {trip_data['days']} days")
        st.write(f"**Budget Level**: {trip_data['budget']}")
        st.write(f"**Traveler Type**: {trip_data['traveler_type']}")
        # Add more detailed plan content here (e.g., itinerary, notes) if needed
    else:
        st.warning("No trip plan generated yet. Please go to the Plan Trip page to create one.")
        st.stop()

    # Add hotel recommendations with beautifully styled cards
    st.subheader("Recommended Hotels")

    # Enhanced CSS for beautifully styled hotel cards
    st.markdown(
        """
        <style>
        .hotel-card {
            background-color: #424242;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            color: #E0E0E0;
            border: 1px solid #616161;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            cursor: pointer;
        }
        .hotel-card:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        .hotel-card img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 10px 10px 0 0;
        }
        .hotel-card .content {
            padding: 10px;
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
            z-index: 1;
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
        {"name": "Hotel One Karachi", "location": "Karachi, Sindh", "google_maps_link": "https://maps.google.com/?q=Hotel+One+Karachi", "image": "https://via.placeholder.com/300x150?text=Hotel+One+Karachi"},
        {"name": "Serena Hotel Thatta", "location": "Thatta, Sindh", "google_maps_link": "https://maps.google.com/?q=Serena+Hotel+Thatta", "image": "https://via.placeholder.com/300x150?text=Serena+Hotel+Thatta"},
        # Add more hotels as needed
    ]
    for hotel in hotels:
        st.markdown(
            f"""
            <a href="{hotel['google_maps_link']}" target="_blank" style="text-decoration: none;">
                <div class="hotel-card">
                    <img src="{hotel['image']}" alt="{hotel['name']} image">
                    <div class="content">
                        <h3>{hotel['name']}</h3>
                        <p>{hotel['location']}</p>
                    </div>
                    <span class="maps-link">View on Google Maps</span>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()