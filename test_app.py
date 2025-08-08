<<<<<<< HEAD
#!/usr/bin/env python3
"""
Simple test script for the Random Long Route Flask application
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Flask application")
        print("Make sure the app is running on http://localhost:5000")
        return False

def test_random_route_endpoint():
    """Test the random route endpoint"""
    try:
        # Test with sample locations
        params = {
            'start': 'Delhi, India',
            'end': 'Mumbai, India'
        }
        
        response = requests.get('http://localhost:5000/get-random-route', params=params)
        print(f"Random route status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Success! Route generated:")
            print(f"Waypoints: {data['waypoints']}")
            print(f"Polyline length: {len(data['polyline'])} characters")
            return True
        else:
            print(f"Error response: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Flask application")
        return False

def main():
    """Run all tests"""
    print("Testing Random Long Route Flask Application")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n❌ Health check failed. Please ensure the application is running.")
        return
    
    print("\n✅ Health check passed!")
    
    # Test random route endpoint
    print("\n2. Testing random route endpoint...")
    route_ok = test_random_route_endpoint()
    
    if route_ok:
        print("\n✅ Random route test passed!")
        print("\n🎉 All tests passed! The application is working correctly.")
    else:
        print("\n❌ Random route test failed.")
        print("This might be due to:")
        print("- Missing or invalid Google Maps API key")
        print("- Missing cities_with_groups.csv file")
        print("- Network connectivity issues")

if __name__ == '__main__':
    main()
=======
#!/usr/bin/env python3
"""
Simple test script for the Random Long Route Flask application
"""

import requests
import json
import time

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"Health check status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Flask application")
        print("Make sure the app is running on http://localhost:5000")
        return False

def test_random_route_endpoint():
    """Test the random route endpoint"""
    try:
        # Test with sample locations
        params = {
            'start': 'Delhi, India',
            'end': 'Mumbai, India'
        }
        
        response = requests.get('http://localhost:5000/get-random-route', params=params)
        print(f"Random route status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Success! Route generated:")
            print(f"Waypoints: {data['waypoints']}")
            print(f"Polyline length: {len(data['polyline'])} characters")
            return True
        else:
            print(f"Error response: {response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Flask application")
        return False

def main():
    """Run all tests"""
    print("Testing Random Long Route Flask Application")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n❌ Health check failed. Please ensure the application is running.")
        return
    
    print("\n✅ Health check passed!")
    
    # Test random route endpoint
    print("\n2. Testing random route endpoint...")
    route_ok = test_random_route_endpoint()
    
    if route_ok:
        print("\n✅ Random route test passed!")
        print("\n🎉 All tests passed! The application is working correctly.")
    else:
        print("\n❌ Random route test failed.")
        print("This might be due to:")
        print("- Missing or invalid Google Maps API key")
        print("- Missing cities_with_groups.csv file")
        print("- Network connectivity issues")

if __name__ == '__main__':
    main()
>>>>>>> 0b6321ae6c39a3fc250c3fe7cadb4514471036ed
