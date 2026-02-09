
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
dbconnect = sqlite3.connect("sensorDB.db")

# Load sensor data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM sensordata", dbconnect)

# Close the database connection
dbconnect.close()

# Convert timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Create the plot with two Y-axes
fig, ax1 = plt.subplots()

# Temperature and Humidity (left Y-axis)
ax1.plot(df['timestamp'], df['temperature'], label='Temperature (°C)')
ax1.plot(df['timestamp'], df['humidity'], label='Humidity (%)')
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature / Humidity")
ax1.legend(loc='upper left')

# Pressure (right Y-axis)
ax2 = ax1.twinx()
ax2.plot(df['timestamp'], df['pressure'], label='Pressure (hPa)', linestyle='dashed')
ax2.set_ylabel("Pressure (hPa)")
ax2.legend(loc='upper right')

# Title and formatting
plt.title("SenseHAT Sensor Data Over Time")
fig.autofmt_xdate()
fig.tight_layout()

# Saves and show the plot
plt.savefig("lab2-database-plot.png")
plt.show()

print("Plot saved as lab2-database-plot.png")

