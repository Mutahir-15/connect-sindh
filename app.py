# Connect Sindh this is our AI Powered trip planner.
import streamlit as st
from utils.auth import handle_oauth_callback, is_authenticated

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    if st.button("Home", key="nav_home"):
        pass  # If already on Home page
    if st.button("Plan Trip", key="nav_plan_trip"):
        st.switch_page("pages/plan_trip.py")
    if "trip_data" in st.session_state and st.button("View Trip", key="nav_view_trip"):
        st.switch_page("pages/view_trip.py")
    if is_authenticated() and st.button("Sign Out", key="sign_out"):
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()

# Custom CSS styling applied here
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    .stApp {
        background: linear-gradient(to bottom, #212121, #303030), url('https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Sindh_district_map.png/800px-Sindh_district_map.png');
        background-blend-mode: overlay;
        background-size: cover;
        background-position: center;
        font-family: 'Roboto', sans-serif;
        color: #E0E0E0;
    }
    .teaser {
        text: left; 
        margin: 15px 0;
        color: #CFD8DC;
    }
    .teaser-item {
        display: inline-block;
        margin: 0 10px;
        font-size: 16px;
    }
    .caption {
        text-align: left;
        color: #B0BEC5;
        font-size: 14px;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Landing page title and description
st.title("CONNECT - Sindh AI-Powered Travel Planner 🌍✈️")
st.write("Welcome to CONNECT, your AI-powered travel planner for Sindh and beyond! Sign in to start planning your trip.")
st.write("**Tagline:** Explore Sindh Smartly with AI")

# Teaser section
st.markdown(
    """
    <div class="teaser">
        Highlighted Cities: 
        <span class="teaser-item">🏜️ Mohenjo-Daro</span>
        <span class="teaser-item">🏙️ Karachi</span>
        <span class="teaser-item">🏞️ Thatta</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Authentication
if not is_authenticated():
    auth_url = handle_oauth_callback()
    if auth_url:
        st.markdown(
            """
            <p style="color: #D32F2F;">Please sign in to continue.</p>
            <a href="{auth_url}" target="_self" style="text-decoration: none;">
                <button style="background-color: #4285F4; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                    <img src="https://www.google.com/favicon.ico" style="width: 20px; vertical-align: middle; margin-right: 10px;" alt="Google logo">
                    Sign in with Google
                </button>
            </a>
            """.format(auth_url=auth_url),
            unsafe_allow_html=True
        )
    else:
        st.error("Failed to initialize OAuth. Please check logs for details.")
else:
    st.success("You are signed in! Use the sidebar to navigate.")

st.markdown('<p class="caption">CONNECT-SINDH an AI Trip Planner by EcoVanguards</p>', unsafe_allow_html=True)
