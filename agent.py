from google.adk.agents import Agent, SequentialAgent, LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search, agent_tool
from google.genai import types
from dotenv import load_dotenv
from datetime import date, datetime
import requests
import os
from typing import Optional


def get_current_date_time() -> str:
    """
    Returns the current date and time in a human-readable format.
    Example: Tuesday, August 19, 2025 - 10:30 PM
    """
    print("* In get_current_date_time()")
    return datetime.now().strftime("%A, %B %d, %Y - %I:%M %p")

def _make_weather_api_request(endpoint: str, params: dict) -> Optional[dict]:
    """
    Helper function to make requests to the WeatherAPI.
    """
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")

    if not api_key:
        print("Error: WEATHER_API_KEY not found in .env file.")
        return None

    base_url = "http://api.weatherapi.com/v1"
    url = f"{base_url}/{endpoint}"
    
    # Add api key to params
    params['key'] = api_key

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def get_current_weather(location: str) -> Optional[dict]:
    """
    Retrieves the real-time weather conditions for a specific location.

    This function queries the /v1/current.json endpoint of the WeatherAPI.

    Args:
        location (str): The location query. Can be one of the following:
                        - Latitude and Longitude (e.g., "48.8567,2.3508")
                        - City name (e.g., "Paris")
                        - US ZIP code (e.g., "90210")
                        - UK postcode (e.g., "SW1")
                        - Canada postal code (e.g., "G2J")
                        - 3-letter IATA airport code (e.g., "LHR")
                        - METAR code (e.g., "metar:EGLL")
                        - IP address (e.g., "100.0.0.1")
                        - `auto:ip` to auto-detect the user's location from their IP.

    Returns:
        dict: A dictionary containing the location and current weather data.
              Returns None if the request fails.
              
              The dictionary contains the following keys:
              - "location": {
                  "name": str,
                  "region": str,
                  "country": str,
                  "lat": float,
                  "lon": float,
                  "tz_id": str,
                  "localtime_epoch": int,
                  "localtime": str
                }
              - "current": {
                  "last_updated_epoch": int,
                  "last_updated": str,
                  "temp_c": float,
                  "temp_f": float,
                  "is_day": int,
                  "condition": {
                      "text": str,
                      "icon": str,
                      "code": int
                  },
                  "wind_mph": float,
                  "wind_kph": float,
                  "wind_degree": int,
                  "wind_dir": str,
                  "pressure_mb": float,
                  "pressure_in": float,
                  "precip_mm": float,
                  "precip_in": float,
                  "humidity": int,
                  "cloud": int,
                  "feelslike_c": float,
                  "feelslike_f": float,
                  "windchill_c": float,
                  "windchill_f": float,
                  "heatindex_c": float,
                  "heatindex_f": float,
                  "dewpoint_c": float,
                  "dewpoint_f": float,
                  "vis_km": float,
                  "vis_miles": float,
                  "uv": float,
                  "gust_mph": float,
                  "gust_kph": float,
                  "short_rad": float,
                  "diff_rad": float,
                  "dni": float,
                  "gti": float
                }
    """
    print(f"* In get_current_weather({location})")
    params = {"q": location, "aqi": "no"}
    return _make_weather_api_request("current.json", params)

def get_weather_forecast(location: str, days: int) -> Optional[dict]:
    """
    Retrieves the weather forecast for a given location up to 14 days.

    This function queries the /v1/forecast.json endpoint of the WeatherAPI.

    Args:
        location (str): The location query. Can be one of the following:
                        - Latitude and Longitude (e.g., "48.8567,2.3508")
                        - City name (e.g., "Paris")
                        - US ZIP code (e.g., "90210")
                        - UK postcode (e.g., "SW1")
                        - Canada postal code (e.g., "G2J")
                        - 3-letter IATA airport code (e.g., "LHR")
                        - METAR code (e.g., "metar:EGLL")
                        - IP address (e.g., "100.0.0.1")
                        - `auto:ip` to auto-detect the user's location from their IP.
        days (int): The number of days to forecast, from 1 to 14.

    Returns:
        dict: A dictionary containing location, current weather, and forecast data.
              Returns None if the request fails.

              The dictionary contains the following keys:
              - "location": (See get_current_weather docstring)
              - "current": (See get_current_weather docstring)
              - "forecast": {
                  "forecastday": [
                    {
                      "date": str,
                      "date_epoch": int,
                      "day": {
                          "maxtemp_c": float, "maxtemp_f": float,
                          "mintemp_c": float, "mintemp_f": float,
                          "avgtemp_c": float, "avgtemp_f": float,
                          "maxwind_mph": float, "maxwind_kph": float,
                          "totalprecip_mm": float, "totalprecip_in": float,
                          "totalsnow_cm": float,
                          "avgvis_km": float, "avgvis_miles": float,
                          "avghumidity": int,
                          "daily_will_it_rain": int, "daily_chance_of_rain": int,
                          "daily_will_it_snow": int, "daily_chance_of_snow": int,
                          "condition": {"text": str, "icon": str, "code": int},
                          "uv": float
                      },
                      "astro": {
                          "sunrise": str, "sunset": str,
                          "moonrise": str, "moonset": str,
                          "moon_phase": str, "moon_illumination": int,
                          "is_moon_up": int, "is_sun_up": int
                      },
                      "hour": [
                        {
                          "time_epoch": int, "time": str,
                          "temp_c": float, "temp_f": float,
                          "is_day": int,
                          "condition": {"text": str, "icon": str, "code": int},
                          "wind_mph": float, "wind_kph": float,
                          "wind_degree": int, "wind_dir": str,
                          "pressure_mb": float, "pressure_in": float,
                          "precip_mm": float, "precip_in": float,
                          "snow_cm": float, "humidity": int, "cloud": int,
                          "feelslike_c": float, "feelslike_f": float,
                          "windchill_c": float, "windchill_f": float,
                          "heatindex_c": float, "heatindex_f": float,
                          "dewpoint_c": float, "dewpoint_f": float,
                          "will_it_rain": int, "chance_of_rain": int,
                          "will_it_snow": int, "chance_of_snow": int,
                          "vis_km": float, "vis_miles": float,
                          "gust_mph": float, "gust_kph": float,
                          "uv": float,
                          "short_rad": float, "diff_rad": float,
                          "dni": float, "gti": float
                        }
                      ]
                    }
                  ]
                }
    """
    print(f"* In get_weather_forecast(location: {location}, days: {days})")
    params = {"q": location, "days": days, "aqi": "no", "alerts": "no"}
    return _make_weather_api_request("forecast.json", params)

def get_astronomy(location: str, dt: Optional[str] = None) -> Optional[dict]:
    """
    Retrieves astronomy data for a location and date.

    This function queries the /v1/astronomy.json endpoint of the WeatherAPI.

    Args:
        location (str): The location query. Can be one of the following:
                        - Latitude and Longitude (e.g., "48.8567,2.3508")
                        - City name (e.g., "Paris")
                        - US ZIP code (e.g., "90210")
                        - UK postcode (e.g., "SW1")
                        - Canada postal code (e.g., "G2J")
                        - 3-letter IATA airport code (e.g., "LHR")
                        - METAR code (e.g., "metar:EGLL")
                        - IP address (e.g., "100.0.0.1")
                        - `auto:ip` to auto-detect the user's location from their IP.
        dt (str, optional): The date in "YYYY-MM-DD" format. Defaults to today.

    Returns:
        dict: A dictionary containing location and astronomy information.
              Returns None if the request fails.

              The dictionary contains the following keys:
              - "location": (See get_current_weather docstring)
              - "astronomy": {
                  "astro": {
                      "sunrise": str,
                      "sunset": str,
                      "moonrise": str,
                      "moonset": str,
                      "moon_phase": str,
                      "moon_illumination": int,
                      "is_moon_up": int,
                      "is_sun_up": int
                  }
                }
    """
    print(f"* In get_astronomy(location: {location}, date: {dt})")

    if dt is None:
        dt = date.today().strftime("%Y-%m-%d")
        
    params = {"q": location, "dt": dt}
    return _make_weather_api_request("astronomy.json", params)




fact_finder_agent = LlmAgent(
    name="fact_finder",    
    model="gemini-2.5-flash",
    description="Agent to look up facts about activities and locations.",
    tools=[google_search],
    instruction=
"""
You are an expert in researching specific facts about activities and locations.

Your job is use Google Search to find answers to specific questions provided to you.

Use the google_search tool to ask your question. Only accept answers with a high degree of confidence.

"""
)



should_i_agent = LlmAgent(
    name="should_i",
    model="gemini-2.5-pro",
    description="This agent accesses current weather conditions, future weather conditions, and astronomical conditions, to help advise a user on whether they should do a certain activity.",
    output_key="advice",

#    tools=[agent_tool.AgentTool(agent=current_weather_agent), agent_tool.AgentTool(agent=weather_forecast_agent)],
    tools=[get_current_weather, get_weather_forecast, get_current_date_time, get_astronomy,
           agent_tool.AgentTool(agent=fact_finder_agent)],

    instruction=
"""

You are a helpful assistant, specializing in advising someone on whether it's a good idea or not for them to participate in a specified activity. Through your tools, you have access to the current weather, future weather forecasts, and astronomical conditions from all around the world. You also have access to a Fact Finder to learn more about the activity or location, if needed.

Your process is:
 - Examine your tools to make sure you thoroughly understand their capabilities.
 - Consider what weather and/or astronomical conditions are conducive to the activity being asked about.
 - Use your tools to gather relevant information.
 - When you feel you have enough information to render credible advice, do so in this format:
   - Tool Use: [List each tool that you used, WHY you chose to use it, and what information you obtained from it]
   - Analysis: [your rationale for your advice]
   - Advice: [your advice]

 """,

)


request_clarifier_agent = LlmAgent(
    name="request_clarifier",
    model="gemini-2.5-pro",
    description="This agent chats with the user until it has enough information to pass along to the should_i agent.",
    sub_agents=[should_i_agent],
    instruction=
"""

You are a friendly chatbot. Your job is to have a conversation with a user in order to find out three things:
 - An activity they want to do
 - When they want to do it
 - Where they want to do it

 When you think you know all of the above:
  - Confirm with the user that you have it right
  - Pass a summary on to should_i_agent
 
 """,

)



# this line determines which agent gets called first
root_agent = request_clarifier_agent
