<<<<<<< HEAD
import os
import traceback
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import googlemaps
from dotenv import load_dotenv

print("--- Script starting ---")

# --- 1. LOAD API KEY ---
try:
    print("Step 1: Loading .env file...")
    if not os.path.exists('.env'):
        print("FATAL ERROR: .env file not found. Please create it.")
        exit() # Stop the script immediately
    
    load_dotenv()
    API_KEY = os.getenv("Maps_API_KEY")
    if not API_KEY:
        print("FATAL ERROR: Maps_API_KEY not found inside .env file.")
        exit()
    print("API Key loaded successfully.")
except Exception as e:
    print(f"FATAL ERROR during API key loading: {e}")
    exit()

# --- 2. LOAD CITY DATA ---
df_cities = None
try:
    print("Step 2: Loading cities_with_groups.csv...")
    csv_path = 'cities_with_groups.csv'
    if not os.path.exists(csv_path):
        print(f"FATAL ERROR: {csv_path} not found in the current directory.")
        exit()
        
    df_cities = pd.read_csv(csv_path)
    print(f"Loaded {len(df_cities)} cities successfully.")
except Exception as e:
    print(f"FATAL ERROR during CSV loading: {e}")
    exit()

# --- 3. INITIALIZE GOOGLE MAPS CLIENT ---
gmaps = None
try:
    print("Step 3: Initializing Google Maps client...")
    gmaps = googlemaps.Client(key=API_KEY)
    print("Google Maps client initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR during Google Maps client initialization: {e}")
    exit()

# --- 4. INITIALIZE FLASK APP ---
app = Flask(__name__)
CORS(app)
print("Flask app initialized.")

# --- HELPER FUNCTION ---
def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371 # Radius of earth in kilometers.
    return c * r

# --- API ENDPOINT ---
@app.route('/get-random-route', methods=['GET'])
def get_random_route():
    # This part of the code will only run when a request is made
    # (The code above runs only once at startup)
    start_location_str = request.args.get('start')
    end_location_str = request.args.get('end')

    if not start_location_str or not end_location_str:
        return jsonify({"error": "Missing 'start' or 'end' parameter"}), 400

    try:
        start_geocode = gmaps.geocode(start_location_str)
        if not start_geocode:
            return jsonify({"error": f"Could not find start location: {start_location_str}"}), 404
        start_coords = start_geocode[0]['geometry']['location']

        end_geocode = gmaps.geocode(end_location_str)
        if not end_geocode:
            return jsonify({"error": f"Could not find end location: {end_location_str}"}), 404
        end_coords = end_geocode[0]['geometry']['location']

        distances = haversine(start_coords['lat'], start_coords['lng'], df_cities['lat'].values, df_cities['lng'].values)
        nearest_city_index = np.argmin(distances)
        landmass_group = df_cities.iloc[nearest_city_index]['landmass_group']
        print(f"Determined landmass group: {landmass_group}")

        df_filtered = df_cities[df_cities['iso2'] == 'IN']
        
        if len(df_filtered) < 3:
             return jsonify({"error": "Not enough cities in India in the dataset."}), 404

        waypoints_df = df_filtered.sample(n=3)
        
        waypoint_coords = [{'lat': float(row['lat']), 'lng': float(row['lng'])} for _, row in waypoints_df.iterrows()]
        waypoint_names = waypoints_df['city'].tolist()
        print(f"Selected waypoints in India: {waypoint_names}")

        directions_result = gmaps.directions(
            origin=start_coords,
            destination=end_coords,
            waypoints=waypoint_coords,
            mode="driving"
        )
        
        if not directions_result:
            return jsonify({"error": "No route found. The random waypoints may be impossible."}), 500

        polyline = directions_result[0]['overview_polyline']['points']
        
        return jsonify({"waypoints": waypoint_names, "polyline": polyline})

    except Exception as e:
        print(f"An unexpected error occurred during request: {e}")
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500

# --- RUN THE APP ---
if __name__ == '__main__':
    print("--- Starting Flask Server ---")
=======
import os
import traceback
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import googlemaps
from dotenv import load_dotenv

print("--- Script starting ---")

# --- 1. LOAD API KEY ---
try:
    print("Step 1: Loading .env file...")
    if not os.path.exists('.env'):
        print("FATAL ERROR: .env file not found. Please create it.")
        exit() # Stop the script immediately
    
    load_dotenv()
    API_KEY = os.getenv("Maps_API_KEY")
    if not API_KEY:
        print("FATAL ERROR: Maps_API_KEY not found inside .env file.")
        exit()
    print("API Key loaded successfully.")
except Exception as e:
    print(f"FATAL ERROR during API key loading: {e}")
    exit()

# --- 2. LOAD CITY DATA ---
df_cities = None
try:
    print("Step 2: Loading cities_with_groups.csv...")
    csv_path = 'cities_with_groups.csv'
    if not os.path.exists(csv_path):
        print(f"FATAL ERROR: {csv_path} not found in the current directory.")
        exit()
        
    df_cities = pd.read_csv(csv_path)
    print(f"Loaded {len(df_cities)} cities successfully.")
except Exception as e:
    print(f"FATAL ERROR during CSV loading: {e}")
    exit()

# --- 3. INITIALIZE GOOGLE MAPS CLIENT ---
gmaps = None
try:
    print("Step 3: Initializing Google Maps client...")
    gmaps = googlemaps.Client(key=API_KEY)
    print("Google Maps client initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR during Google Maps client initialization: {e}")
    exit()

# --- 4. INITIALIZE FLASK APP ---
app = Flask(__name__)
CORS(app)
print("Flask app initialized.")

# --- HELPER FUNCTION ---
def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371 # Radius of earth in kilometers.
    return c * r

# --- API ENDPOINT ---
@app.route('/get-random-route', methods=['GET'])
def get_random_route():
    # This part of the code will only run when a request is made
    # (The code above runs only once at startup)
    start_location_str = request.args.get('start')
    end_location_str = request.args.get('end')

    if not start_location_str or not end_location_str:
        return jsonify({"error": "Missing 'start' or 'end' parameter"}), 400

    try:
        start_geocode = gmaps.geocode(start_location_str)
        if not start_geocode:
            return jsonify({"error": f"Could not find start location: {start_location_str}"}), 404
        start_coords = start_geocode[0]['geometry']['location']

        end_geocode = gmaps.geocode(end_location_str)
        if not end_geocode:
            return jsonify({"error": f"Could not find end location: {end_location_str}"}), 404
        end_coords = end_geocode[0]['geometry']['location']

        distances = haversine(start_coords['lat'], start_coords['lng'], df_cities['lat'].values, df_cities['lng'].values)
        nearest_city_index = np.argmin(distances)
        landmass_group = df_cities.iloc[nearest_city_index]['landmass_group']
        print(f"Determined landmass group: {landmass_group}")

        df_filtered = df_cities[df_cities['iso2'] == 'IN']
        
        if len(df_filtered) < 3:
             return jsonify({"error": "Not enough cities in India in the dataset."}), 404

        waypoints_df = df_filtered.sample(n=3)
        
        waypoint_coords = [{'lat': float(row['lat']), 'lng': float(row['lng'])} for _, row in waypoints_df.iterrows()]
        waypoint_names = waypoints_df['city'].tolist()
        print(f"Selected waypoints in India: {waypoint_names}")

        directions_result = gmaps.directions(
            origin=start_coords,
            destination=end_coords,
            waypoints=waypoint_coords,
            mode="driving"
        )
        
        if not directions_result:
            return jsonify({"error": "No route found. The random waypoints may be impossible."}), 500

        polyline = directions_result[0]['overview_polyline']['points']
        
        return jsonify({"waypoints": waypoint_names, "polyline": polyline})

    except Exception as e:
        print(f"An unexpected error occurred during request: {e}")
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500

# --- RUN THE APP ---
if __name__ == '__main__':
    print("--- Starting Flask Server ---")
>>>>>>> 0b6321ae6c39a3fc250c3fe7cadb4514471036ed
    app.run(debug=True)