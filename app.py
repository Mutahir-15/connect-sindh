
import streamlit as st
from utils.auth import handle_oauth_callback, is_authenticated, initiate_oauth_flow

# Detect the current path using st.query_params
query_params = st.query_params
current_path = query_params.get("path", [""])[0]
if not current_path.startswith("/"):
    current_path = f"/{current_path}"

# Sidebar navigation
with st.sidebar:
    st.header("Navigation")
    if st.button("Home", key="nav_home"):
        st.query_params.clear()
        st.query_params.update({"path": "/"})
        st.rerun()
    if st.button("Plan Trip", key="nav_plan_trip"):
        st.switch_page("pages/plan_trip.py")
    if "trip_data" in st.session_state and st.button("View Trip", key="nav_view_trip"):
        st.switch_page("pages/view_trip.py")
    if is_authenticated() and st.button("Sign Out", key="sign_out"):
        st.session_state.clear()
        st.query_params.clear()
        st.rerun()

# Custom CSS for styling with background image
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
    h1 {
        color: #1E88E5;
        font-weight: 700;
        text-align: center;
        margin-bottom: 10px;
    }
    p {
        text-align: center;
        margin: 10px 0;
    }
    .stButton>button {
        background-color: #4285F4;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 500;
        display: block;
        margin: 20px auto;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
    .caption {
        text-align: center;
        color: #B0BEC5;
        font-size: 14px;
        margin-top: 20px;
    }
    .teaser {
        text-align: center;
        margin: 20px 0;
        color: #CFD8DC;
    }
    .teaser-item {
        display: inline-block;
        margin: 0 15px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Handle the /oauth2callback route
if current_path == "/oauth2callback":
    if not is_authenticated():
        handle_oauth_callback()  # Process the OAuth callback
    st.query_params.clear()
    st.query_params.update({"path": "/"})
    st.rerun()

# Main home page
if current_path == "/":
    st.title("CONNECT - Sindh AI-Powered Travel Planner 🌍✈️")
    st.write("Welcome to CONNECT, your AI-powered travel planner for Sindh and beyond! Sign in to start planning your trip.")
    st.write("**Tagline:** Explore Sindh Smartly with AI")

    # Teaser section
    st.markdown(
        """
        <div class="teaser">
            Highlighted Destinations: 
            <span class="teaser-item">🏜️ Mohenjo-Daro</span>
            <span class="teaser-item">🏙️ Karachi</span>
            <span class="teaser-item">🏞️ Thatta</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not is_authenticated():
        auth_url = initiate_oauth_flow()
        if auth_url:
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <button id="google-signin" style="background-color: #4285F4; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                        <img src="https://www.google.com/favicon.ico" style="width: 20px; vertical-align: middle; margin-right: 10px;" alt="Google logo">
                        Sign in with Google
                    </button>
                    <script>
                        document.getElementById('google-signin').addEventListener('click', function() {{
                            window.open('{auth_url}', 'OAuthPopup', 'width=500,height=600');
                        }});
                    </script>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.success("You are signed in! Use the sidebar to navigate.")

    st.markdown('<p class="caption">CONNECT-SINDH an AI Trip Planner by EcoVanguards</p>', unsafe_allow_html=True)