# CONNECT - SINDH an AI Trip Planner, Google Solution Challenge 2025
import streamlit as st
from utils.auth import handle_oauth_callback, is_authenticated, initiate_oauth_flow
import os

# Detect the current path using st.query_params
query_params = st.query_params
current_path = query_params.get("path", [""])[0]
if not current_path.startswith("/"):
    current_path = f"/{current_path}"

# Sidebar navigation with custom styling
with st.sidebar:
    st.markdown("### 🚀 CONNECT - SINDH")
    st.write("🌍 Navigation")

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

# Inject custom CSS (unchanged)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    .stApp {
        background: linear-gradient(to bottom, #212121, #303030),
                    url('https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Sindh_district_map.png/800px-Sindh_district_map.png');
        background-blend-mode: overlay;
        background-size: cover;
        background-position: center;
        font-family: 'Roboto', sans-serif;
        color: #E0E0E0;
    }

    h1 {
        color: #1E88E5;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }

    p {
        text-align: center;
        margin: 15px 0;
    }

    .stButton>button {
        background-color: #4285F4;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 500;
        display: block;
        margin: 30px auto;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }

    section[data-testid="stSidebar"] {
        background-color: #2E2E2E;
        border-right: 1px solid #424242;
    }

    section[data-testid="stSidebar"] .stButton>button {
        background-color: #616161;
        color: white;
        border: none;
        padding: 8px 16px;
        margin: 8px 0;
        width: 100%;
        border-radius: 6px;
        font-weight: 500;
        transition: background-color 0.3s ease;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background-color: #757575;
    }

    .caption {
        text-align: center;
        color: #B0BEC5;
        font-size: 14px;
        margin-top: 30px;
    }

    .teaser {
        text-align: center;
        margin: 30px 0;
        color: #CFD8DC;
        font-size: 16px;
    }

    .teaser span {
        display: inline-block;
        margin: 0 12px;
    }

    .debug {
        text-align: center;
        color: #FF5722;
        font-size: 14px;
        word-wrap: break-word;
        margin: 15px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Handle OAuth callback
if current_path == "/oauth2callback":
    if handle_oauth_callback() is None:
        st.error("Authentication failed or callback incomplete. Redirecting to home.")
        st.query_params.clear()
        st.query_params.update({"path": "/"})
        st.rerun()
    elif is_authenticated():
        st.switch_page("pages/plan_trip.py")
    else:
        st.rerun()

# Main home page
st.markdown(
    """
    <div style="text-align: center; margin-top: 40px;">
        <h1 style="color: #1E88E5; font-size: 36px; font-weight: bold; margin-bottom: 10px;">
            CONNECT - Sindh AI-Powered Travel Planner 🌍✈️
        </h1>
        <p style="font-size: 18px; color: #E0E0E0;">
            Welcome to <strong>CONNECT</strong>, your AI-powered travel planner for Sindh and beyond!
        </p>
        <p style="font-size: 16px; margin-bottom: 30px; color: #B0BEC5;">
            <em>Tagline: Explore Sindh Smartly with AI</em>
        </p>
        <div class="teaser">
            <strong style="color: #CFD8DC;">Highlighted Destinations:</strong><br><br>
            <span class="teaser-item">🏜️ Mohenjo-Daro</span>  
            <span class="teaser-item">🏙️ Karachi</span>  
            <span class="teaser-item">🏞️ Thatta</span>
        </div>
    """,
    unsafe_allow_html=True
)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
st.write(f"Debug: GOOGLE_CLIENT_ID = {GOOGLE_CLIENT_ID[:5]}...") 
st.write(f"Debug: GOOGLE_CLIENT_SECRET = {GOOGLE_CLIENT_SECRET[:5]}...") 

if not is_authenticated():
    auth_url = initiate_oauth_flow()
    if auth_url:
        st.markdown(
            f"""<div style="text-align: center; margin-top: 40px; margin-bottom: 50px;">
                <a href="{auth_url}" target="_self">
                    <button style="background-color: #4285F4; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: 500;">
                        <img src="https://www.google.com/favicon.ico" style="width: 20px; vertical-align: middle; margin-right: 10px;" alt="Google logo">
                        Sign in with Google
                    </button>
                </a>
            </div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div class="debug">Error: Authentication URL not generated. Check logs.</div>', unsafe_allow_html=True)
else:
    st.success("✅ You are signed in! Use the sidebar to navigate and start your journey.")

st.markdown(
    """<p class="caption" style="margin-top: 50px;">CONNECT-SINDH — An AI Trip Planner by EcoVanguards</p>
    </div>""",
    unsafe_allow_html=True
)