from flask import Flask, request, jsonify
import pandas as pd
import googlemaps
import os
import random
from dotenv import load_dotenv
import math

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global variables to store data
cities_df = None
gmaps = None

def load_data():
    """Load cities data and initialize Google Maps client on startup"""
    global cities_df, gmaps
    
    # Load cities data from CSV
    try:
        cities_df = pd.read_csv('cities_with_groups.csv')
        print(f"Loaded {len(cities_df)} cities from CSV")
    except FileNotFoundError:
        print("Warning: cities_with_groups.csv not found. Please ensure the file exists.")
        cities_df = pd.DataFrame(columns=['city', 'lat', 'lng', 'landmass_group'])
    
    # Initialize Google Maps client
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY not found in environment variables")
    
    gmaps = googlemaps.Client(key=api_key)
    print("Google Maps client initialized successfully")

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def find_nearest_city(lat, lng):
    """Find the nearest city from our dataset to given coordinates"""
    if cities_df.empty:
        return None
    
    min_distance = float('inf')
    nearest_city = None
    
    for _, row in cities_df.iterrows():
        distance = calculate_distance(lat, lng, row['lat'], row['lng'])
        if distance < min_distance:
            min_distance = distance
            nearest_city = row
    
    return nearest_city

def geocode_location(location_string):
    """Geocode a location string to get coordinates"""
    try:
        geocode_result = gmaps.geocode(location_string)
        if not geocode_result:
            return None, "Location not found"
        
        location = geocode_result[0]['geometry']['location']
        return location, None
    except Exception as e:
        return None, f"Geocoding error: {str(e)}"

def get_landmass_group(lat, lng):
    """Determine the landmass group for given coordinates"""
    nearest_city = find_nearest_city(lat, lng)
    if nearest_city is None:
        return None, "No nearby cities found in dataset"
    
    return nearest_city['landmass_group'], None

def select_random_waypoints(landmass_group, count=3):
    """Select random cities from the specified landmass group"""
    # Filter cities by landmass group
    filtered_cities = cities_df[cities_df['landmass_group'] == landmass_group]
    
    if len(filtered_cities) < count:
        return None, f"Not enough cities in landmass group {landmass_group}. Found {len(filtered_cities)}, need {count}"
    
    # Randomly select cities
    selected_cities = filtered_cities.sample(n=count)
    return selected_cities['city'].tolist(), None

def get_route_with_waypoints(start_location, end_location, waypoints):
    """Get route from Google Maps Directions API with waypoints"""
    try:
        # Convert waypoint city names to coordinates
        waypoint_coords = []
        for city in waypoints:
            city_data = cities_df[cities_df['city'] == city].iloc[0]
            waypoint_coords.append(f"{city_data['lat']},{city_data['lng']}")
        
        # Call Directions API
        directions_result = gmaps.directions(
            start_location,
            end_location,
            waypoints=waypoint_coords,
            optimize_waypoints=False  # Keep waypoints in order
        )
        
        if not directions_result:
            return None, "No route found"
        
        # Extract polyline
        polyline = directions_result[0]['overview_polyline']['points']
        return polyline, None
        
    except Exception as e:
        return None, f"Directions API error: {str(e)}"

@app.route('/get-random-route', methods=['GET'])
def get_random_route():
    """Main endpoint to get a random route with waypoints"""
    try:
        # Get query parameters
        start_location = request.args.get('start')
        end_location = request.args.get('end')
        
        # Validate parameters
        if not start_location:
            return jsonify({'error': 'Missing start parameter'}), 400
        if not end_location:
            return jsonify({'error': 'Missing end parameter'}), 400
        
        # Step 1: Geocode start location
        start_coords, error = geocode_location(start_location)
        if error:
            return jsonify({'error': error}), 400
        
        # Step 2: Determine landmass group
        landmass_group, error = get_landmass_group(start_coords['lat'], start_coords['lng'])
        if error:
            return jsonify({'error': error}), 400
        
        # Step 3: Select random waypoints
        waypoints, error = select_random_waypoints(landmass_group)
        if error:
            return jsonify({'error': error}), 400
        
        # Step 4: Get route with waypoints
        polyline, error = get_route_with_waypoints(start_location, end_location, waypoints)
        if error:
            return jsonify({'error': error}), 400
        
        # Step 5: Return success response
        return jsonify({
            'waypoints': waypoints,
            'polyline': polyline
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'cities_loaded': len(cities_df) if cities_df is not None else 0}), 200

if __name__ == '__main__':
    # Load data on startup
    load_data()
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
