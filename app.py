import streamlit as st
import requests
import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
# Load API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialize Google Maps API Client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Function to generate trip plan
def generate_trip_plan(destination, days, budget, traveler_type):
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not found. Check your .env file."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Generate a travel plan for {destination} for {days} days with a {budget} budget for a {traveler_type}."}
                ]
            }
        ],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 500}
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        
        if "candidates" in response_json:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error: {response_json}"
    except requests.exceptions.JSONDecodeError:
        return f"Failed to decode API response: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"

# Function to get hotel recommendations
def get_hotels(destination):
    places_result = gmaps.places(query=f"hotels in {destination}", type="lodging")
    return places_result["results"][:5]

# Streamlit UI
st.title("CONNECT - Sindh AI-Powered Travel Planner 🌍✈️")
destination = st.text_input("Enter Destination", "Mohenjo-Daro")
days = st.slider("Number of Days", 1, 30, 1)
budget = st.selectbox("Budget Level", ["Luxury", "Mid-range", "Budget"])
traveler_type = st.selectbox("Traveler Type", ["Solo", "Couple", "Family", "Group"])

if st.button("Generate Trip Plan"):
    itinerary = generate_trip_plan(destination, days, budget, traveler_type)
    hotels = get_hotels(destination)
    
    st.subheader("🗺️ Generated Itinerary")
    st.text(itinerary)
    
    st.subheader("🏨 Recommended Hotels")
    for hotel in hotels:
        st.text(f"🏨 {hotel['name']} - Rating: {hotel.get('rating', 'N/A')} ⭐")
        st.text(f"📍 Address: {hotel['formatted_address']}")

st.caption("Build by EcoVanguards")