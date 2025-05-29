# Fetch weather ddata from OpenWeatherMap API and save it to a file
import requests

def format_weather_data(weather_data):
    if not weather_data:
        return "No data available"
    
    try:
        city = weather_data.get('name', 'Unknown')
        temperature = weather_data.get('main', {}).get('temp', 'N/A')
        weather_list = weather_data.get('weather', [])
        description = weather_list[0].get('description', 'N/A') if weather_list else 'N/A'
        formatted_data = f"Weather in {city}:\nTemperature: {temperature}°C\nDescription: {description.capitalize()}\n"
    except Exception as e:
        return f"Error formatting weather data: {e}"
    return formatted_data

def fetch_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        return format_weather_data(response.json())
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def save_weather_to_file(weather_data, filename):
    try:
        with open(filename, 'w') as file:
            file.write(weather_data)
    except Exception as e:
        print(f"Error saving weather data to file: {e}")
