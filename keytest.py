import googlemaps
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("Maps_API_KEY")

if not API_KEY:
    print("ERROR: Could not find Maps_API_KEY in your .env file.")
else:
    try:
        print("API Key found. Initializing client...")
        gmaps = googlemaps.Client(key=API_KEY)

        print("Testing a simple directions request from Delhi to Mumbai...")

        # A simple, direct route request
        directions_result = gmaps.directions(
            "Delhi, India",
            "Mumbai, India",
            mode="driving"
        )

        if directions_result:
            print("\n--- ✅ SUCCESS! ---")
            print("The API key is working correctly for a simple route.")
        else:
            print("\n--- ❌ FAILURE ---")
            print("The API call failed. The problem is with your Google Cloud Project or API Key (Billing, Permissions, etc.).")

    except Exception as e:
        print("\n--- ❌ AN ERROR OCCURRED ---")
        print(f"The test failed with an exception: {e}")