
import os
import requests
from dotenv import load_dotenv

def test_weather_api():
    """
    Tests the WeatherAPI connection by fetching the current weather for Denver, CO.
    """
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        print("Error: WEATHER_API_KEY not found in .env file.")
        return

    base_url = "http://api.weatherapi.com/v1"
    endpoint = "current.json"
    url = f"{base_url}/{endpoint}"
    
    params = {
        "key": api_key,
        "q": "Denver",
        "aqi": "no"
    }

    print(f"Requesting URL: {url}")
    print(f"With params: {params}")

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        print("Successfully received a response.")
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print("Status Code:", e.response.status_code)
            print("Response Text:", e.response.text)


if __name__ == "__main__":
    test_weather_api()
