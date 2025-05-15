
import requests
import googlemaps
import os
from utils.config import validate_env

# Validate environment variables
validate_env()

# Load environment variables after validation
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialize Google Maps client safely
try:
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
except ValueError as e:
    raise ValueError(f"Failed to initialize Google Maps client: {str(e)}")

def generate_trip_plan(destination, days, budget, traveler_type):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Generate a travel plan for {destination} for {days} days with a {budget} budget for a {traveler_type}."}
                ]
            }
        ]
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

def get_hotels(destination):
    places_result = gmaps.places(query=f"hotels in {destination}", type="lodging")
    return places_result["results"][:5]
