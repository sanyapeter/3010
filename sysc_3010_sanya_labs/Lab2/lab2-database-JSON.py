from urllib.request import urlopen
from urllib.parse import urlencode
import json
import sqlite3


dbconnect = sqlite3.connect("sensorDB.db")
cursor = dbconnect.cursor()

# Create table Winds if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Winds (
    City TEXT,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    WindSpeed REAL
)
""")


apiKey = "a808bbf30202728efca23e099a4eecc7"
city = input("Enter the name of a city whose weather you want: ")

params = {"q": city, "units": "metric", "APPID": apiKey}
url = "http://api.openweathermap.org/data/2.5/weather?" + urlencode(params)

print(f"Requesting data from URL: {url}")
webData = urlopen(url)
results = webData.read().decode('utf-8')
webData.close()

print("The raw JSON string returned by the query is:")
print(results)

# Parse JSON
data = json.loads(results)

# Extract wind speed
wind_speed = data.get("wind", {}).get("speed", None)


cursor.execute(
    "SELECT WindSpeed FROM Winds WHERE LOWER(City)=? ORDER BY Date DESC LIMIT 1",
    (city.lower(),)
)
current_wind_speed = cursor.fetchone()

if current_wind_speed:
    current_wind_speed = current_wind_speed[0]
    if wind_speed is not None:
        if wind_speed > current_wind_speed:
            comparison_result = "higher"
        elif wind_speed < current_wind_speed:
            comparison_result = "lower"
        else:
            comparison_result = "the same"
        print(f"The new wind speed ({wind_speed} m/s) is {comparison_result} than the most recent wind speed ({current_wind_speed} m/s) recorded for {city}.")
    else:
        print("No wind speed data available for the new record.")
else:
    print(f"No previous wind speed recorded for {city}.")

# Insert new wind speed into the database 
cursor.execute(
    "INSERT INTO Winds (City, WindSpeed) VALUES (?, ?)",
    (city.lower(), wind_speed)
)
dbconnect.commit()

print("Temperature: %d%sC" % (data["main"]["temp"], chr(176)))
print("Humidity: %d%%" % data["main"]["humidity"])
print("Pressure: %d" % data["main"]["pressure"])
print("Wind: %d" % data["wind"]["speed"])

dbconnect.close()
