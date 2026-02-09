import time
import sqlite3
from datetime import datetime
from sense_hat import SenseHat

sense = SenseHat()

# Connect to SQLite database (it will create the file if it doesn't exist)
dbconnect = sqlite3.connect("sensorDB.db")
dbconnect.row_factory = sqlite3.Row
cursor = dbconnect.cursor()

# Create the table if it doesn't exist yet

print("Starting SenseHAT data logging. Press Ctrl+C to stop.")

try:
    while True:
        # Read sensor data
        temperature = round(sense.get_temperature(), 2)
        humidity = round(sense.get_humidity(), 2)
        pressure = round(sense.get_pressure(), 2)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert data into the database
        cursor.execute(
            "INSERT INTO sensordata (timestamp, temperature, humidity, pressure) VALUES (?, ?, ?, ?)",
            (timestamp, temperature, humidity, pressure)
        )
        dbconnect.commit()

        # Print to console 
        print(f"{timestamp} | Temp: {temperature}°C | Humidity: {humidity}% | Pressure: {pressure} hPa")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nLogging stopped by user.")

finally:
    dbconnect.close()

