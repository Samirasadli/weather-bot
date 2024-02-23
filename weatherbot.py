import requests
import pandas as pd
import plotly.express as px

API_KEY = "YOUR_API_KEY"  # Replace with your actual API key


def get_weather_data(city_name):
    """Fetches and parses weather data for a given city.

    Args:
        city_name (str): Name of the city to retrieve weather data for.

    Returns:
        pd.DataFrame: DataFrame containing weather data.

    Raises:
        ValueError: If city name is not provided or invalid.
        requests.exceptions.RequestException: If API request fails.
    """

    if not city_name:
        raise ValueError("Please provide a city name.")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        return _parse_weather_data(data)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city_name}: {e}")
        return None


def _parse_weather_data(data):
    """Parses JSON data from API response into a DataFrame.

    Args:
        data (dict): JSON response from OpenWeatherMap API.

    Returns:
        pd.DataFrame: DataFrame containing weather data.
    """

    return pd.DataFrame({
        "Temperature (°C)": [data["main"]["temp"]],
        "Feels Like (°C)": [data["main"]["feels_like"]],
        "Humidity (%)": [data["main"]["humidity"]],
        "Wind Speed (m/s)": [data["wind"]["speed"]],
        "Precipitation": [data["weather"][0]["main"]],
        "Precipitation Probability (%)": [data["clouds"]["all"]],
    }, index=[0])


def visualize_data(weather_data):
    """Creates and displays visualizations for weather data."""

    temp_chart = px.line(weather_data, x=weather_data.index, y="Temperature (°C)", title="Temperature")
    temp_chart.update_traces(marker_color="red")

    humidity_chart = px.bar(weather_data, x="Humidity (%)", title="Humidity")
    humidity_chart.update_traces(marker_color="teal")

    wind_speed_chart = px.bar(weather_data, x="Wind Speed (m/s)", title="Wind Speed")
    wind_speed_chart.update_traces(marker_color="royalblue")

    temp_chart.show()
    humidity_chart.show()
    wind_speed_chart.show()


def main():
    city_name = input("Enter city name: ")
    weather_data = get_weather_data(city_name)

    if weather_data is not None:
        print(weather_data)
        visualize_data(weather_data)

        precipitation = weather_data.loc[0, "Precipitation"]
        if precipitation in ["Rain", "Drizzle", "Snow", "Snow showers"]:
            print("There's a chance of precipitation today. Be prepared for possible rain in the next few days.")
        elif precipitation in ["Clouds", "Mist", "Smoke", "Haze", "Dust", "Fog"]:
            print("Mostly cloudy today. Rain chances for the next few days are uncertain.")
        else:
            print("Clear skies today. Rain is unlikely in the next few days.")


if __name__ == "__main__":
    main()
