# Random Long Route Flask Application

A Flask backend application that generates random routes with waypoints using the Google Maps API.

## Features

- **Random Route Generation**: Takes start and end locations, finds the landmass, and selects 3 random cities as waypoints
- **Google Maps Integration**: Uses Google Maps Geocoding and Directions APIs
- **Landmass Detection**: Determines the landmass group based on the starting location
- **Efficient Data Loading**: Loads city data once on startup for optimal performance

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root with your Google Maps API key:

```
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

**To get a Google Maps API key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Geocoding API
   - Directions API
4. Create credentials (API Key)
5. Copy the API key to your `.env` file

### 3. Data File

Ensure you have a `cities_with_groups.csv` file in the project root with the following columns:
- `city`: City name
- `lat`: Latitude
- `lng`: Longitude  
- `landmass_group`: Landmass identifier

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## API Endpoints

### GET /get-random-route

Generates a random route with waypoints between two locations.

**Query Parameters:**
- `start` (required): Starting location (e.g., "Delhi, India")
- `end` (required): Destination location (e.g., "Mumbai, India")

**Success Response (200):**
```json
{
  "waypoints": ["CityName1", "CityName2", "CityName3"],
  "polyline": "encoded_polyline_string_from_google"
}
```

**Error Response (400/500):**
```json
{
  "error": "Descriptive error message"
}
```

### GET /health

Health check endpoint to verify the application status.

**Response:**
```json
{
  "status": "healthy",
  "cities_loaded": 1234
}
```

## Example Usage

```bash
# Get a random route from Delhi to Mumbai
curl "http://localhost:5000/get-random-route?start=Delhi,India&end=Mumbai,India"

# Health check
curl "http://localhost:5000/health"
```

## How It Works

1. **Request Processing**: Receives start and end locations as query parameters
2. **Geocoding**: Converts the start location string to coordinates using Google Maps Geocoding API
3. **Landmass Detection**: Finds the nearest city in the dataset to determine the landmass group
4. **Waypoint Selection**: Randomly selects 3 cities from the same landmass group
5. **Route Generation**: Calls Google Maps Directions API with the waypoints
6. **Response**: Returns the waypoint city names and encoded polyline

## Error Handling

The application handles various error scenarios:
- Missing or invalid API key
- Location not found during geocoding
- Insufficient cities in landmass group
- Google Maps API errors
- Missing required parameters

## Dependencies

- **Flask**: Web framework
- **pandas**: Data handling and CSV processing
- **googlemaps**: Google Maps API client
- **python-dotenv**: Environment variable management

## Security Notes

- Never commit your `.env` file to version control
- Keep your Google Maps API key secure
- Consider implementing rate limiting for production use
- Monitor API usage to stay within Google's quotas
