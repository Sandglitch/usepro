@app.route('/get-random-route', methods=['GET'])
def get_random_route():
    start_location_str = request.args.get('start')
    end_location_str = request.args.get('end')

    if not start_location_str or not end_location_str:
        return jsonify({"error": "Missing 'start' or 'end' parameter"}), 400

    try:
        # 1. Geocode start and end locations
        start_geocode = gmaps.geocode(start_location_str)
        if not start_geocode:
            return jsonify({"error": f"Could not find start location: {start_location_str}"}), 404
        start_coords = start_geocode[0]['geometry']['location']

        end_geocode = gmaps.geocode(end_location_str)
        if not end_geocode:
            return jsonify({"error": f"Could not find end location: {end_location_str}"}), 404
        end_coords = end_geocode[0]['geometry']['location']

        # 2. Determine landmass group (still useful for other cases)
        distances = haversine(start_coords['lat'], start_coords['lng'], df_cities['lat'].values, df_cities['lng'].values)
        nearest_city_index = np.argmin(distances)
        landmass_group = df_cities.iloc[nearest_city_index]['landmass_group']
        print(f"Determined landmass group: {landmass_group}")

        # --- THIS IS THE ONLY CHANGE ---
        # Filter the DataFrame to ONLY include cities in India ('IN')
        df_filtered = df_cities[df_cities['iso2'] == 'IN']
        print(f"Found {len(df_filtered)} cities in India to use as waypoints.")
        # --- END OF CHANGE ---
        
        num_available_cities = len(df_filtered)
        if num_available_cities < 3:
             return jsonify({"error": "Not enough cities in India in the dataset to select 3 waypoints."}), 404

        sample_size = 3
        waypoints_df = df_filtered.sample(n=sample_size)
        
        waypoint_coords = [
            {'lat': float(row['lat']), 'lng': float(row['lng'])} 
            for index, row in waypoints_df.iterrows()
        ]
        waypoint_names = waypoints_df['city'].tolist()
        print(f"Selected waypoints within India: {waypoint_names}")

        # 4. Call Directions API using ONLY coordinates
        directions_result = gmaps.directions(
            origin=start_coords,
            destination=end_coords,
            waypoints=waypoint_coords,
            mode="driving"
        )
        
        if not directions_result:
            return jsonify({"error": "No route found even within India. The API key may have severe restrictions."}), 500

        # 5. Extract Polyline and return
        polyline = directions_result[0]['overview_polyline']['points']
        
        return jsonify({
            "waypoints": waypoint_names,
            "polyline": polyline
        })

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        return jsonify({"error": "An internal server error occurred."}), 500