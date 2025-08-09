#Njan aan Map🗺️🗺️


###Team Name: STONKS


### Team Members
- Team Lead: Jerin Joice   - Vishwajyothi college of engineering and technology
- Member 2: Vivek Rajeev - Vishwajyothi college of engineering and technology

### Project Description

Njan Aan Map is a web app that finds a route between two points in India. The route doesn't have to be shortest route or the most optimal route. It will find a 'route' from point A to point B and that's it.

### The Problem (that doesn't exist)
People need to get from point A to point B

### The Solution (that nobody asked for)
We get them from point A to point B...eventually

## Technical Details
### Technologies/Components Used
For Software:
- Python,HTML
- Flask
- pandas,numpy,googlemaps,python-dotenv,Flask-Cors,os,traceback
- Google Maps API,Vercel


### Implementation
For Software:
# Installation
 Install Dependencies

```bash
pip install -r requirements.txt
```

# Run

```bash
python app.py
```

### Project Documentation
For Software:

# Screenshots
<img width="3188" height="1202" alt="frame (3)" src="https://i.postimg.cc/c1BVLcN1/1.webp" />
## Homepage Preview

<img width="3188" height="1202" alt="frame (3)" src="https://i.postimg.cc/c1BVLcN1/2.webp" />
## User enters input

<img width="3188" height="1202" alt="frame (3)" src="https://i.postimg.cc/c1BVLcN1/3.webp" />
## Critically accurate routes are shown


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

