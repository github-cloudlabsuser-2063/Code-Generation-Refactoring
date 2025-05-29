# Fetch weather ddata from OpenWeatherMap API and save it to a file
import requests
import sys
from datetime import datetime  # Add this import

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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python weather_script.py <API_KEY> <CITY_NAME> <OUTPUT_FILE>")
    else:
        api_key = sys.argv[1]
        city = sys.argv[2]
        output_file = sys.argv[3]

        # Add city and datetime to the output file name
        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        city_safe = city.replace(" ", "_")
        file_parts = output_file.rsplit('.', 1)
        if len(file_parts) == 2:
            output_file = f"{file_parts[0]}_{city_safe}_{now_str}.{file_parts[1]}"
        else:
            output_file = f"{output_file}_{city_safe}_{now_str}"

        weather_info = fetch_weather(api_key, city)
        if weather_info:
            save_weather_to_file(weather_info, output_file)
            print(f"Weather data saved to {output_file}")
        else:
            print("Failed to fetch weather data.")
