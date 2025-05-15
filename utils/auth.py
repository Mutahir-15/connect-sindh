import streamlit as st
from google_auth_oauthlib.flow import Flow
import logging
from utils.config import validate_env
import os

# Validate environment variables
validate_env()

# Load environment variables after validation
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
REDIRECT_URI = "https://connect-sindh.streamlit.app/oauth2callback"  
# Ensure client config is valid
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    st.error("OAuth configuration failed: Client ID or Secret missing.")
    st.stop()

CLIENT_CONFIG = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [REDIRECT_URI]
    }
}

def handle_oauth_callback():
    """Handle OAuth authentication and callback."""
    try:
        flow = Flow.from_client_config(
            client_config=CLIENT_CONFIG,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
    except ValueError as e:
        logger.error(f"Failed to initialize OAuth flow: {str(e)}")
        st.error(f"OAuth initialization failed: {str(e)}")
        return None

    auth_url, _ = flow.authorization_url(prompt='consent')
    try:
        query_params = st.query_params.to_dict()
    except Exception as e:
        logger.error(f"Failed to access query parameters: {str(e)}")
        query_params = {}

    if 'code' in query_params:
        try:
            logger.debug(f"Processing OAuth code: {query_params['code']}")
            flow.fetch_token(code=query_params['code'])
            st.session_state.credentials = flow.credentials
            st.session_state.user_info = True
            logger.info("OAuth callback successful")
            # Clear query params after processing
            st.query_params.clear()
            # Rerun after setting session state
            st.rerun()
        except Exception as e:
            logger.error(f"OAuth callback failed: {str(e)}")
            st.error(f"OAuth callback failed: {str(e)}")
    return auth_url

def is_authenticated():
    """Check if the user is authenticated."""
    return 'credentials' in st.session_state and st.session_state.get('user_info', False)

def initiate_oauth_flow():
    """Initiate the OAuth flow by redirecting to the auth URL."""
    auth_url = handle_oauth_callback()
    if auth_url:
        # Use JavaScript to redirect in the same tab
        st.markdown(
            f"""
            <script>
                window.location.href = "{auth_url}";
            </script>
            """,
            unsafe_allow_html=True
        )
