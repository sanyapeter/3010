# Lab 3 – Pyrebase fixed version
import pyrebase
from sense_hat import SenseHat
from datetime import datetime
import time
import os
import json

# Load Firebase configuration from environment variable
try:
    config = json.loads(os.environ['W24SYSC3010LAB3FIREBASECONFIG'])
except KeyError:
    # Fallback: replace with your Firebase details if env var is missing
    config = {
        "apiKey": "AIzaSyC2D_7aOU2d_OK88ExLGT6Qs6QqduK-LTs",
        "authDomain": "sysc3010-ed257.firebaseapp.com",
        "databaseURL": "https://sysc3010-ed257-default-rtdb.firebaseio.com/",
        "storageBucket": "sysc3010-ed257.appspot.com"
    }

# Connect to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Device username and dataset
username = "sanya"
dataset = "sensor1"

#username_lst=[sanya,sydney,jad,rysn sanad]
# Get all usernames dynamically from Firebase
try:
    usernames_data = db.child("users").get()
    username_lst = [user.key() for user in usernames_data.each()]
except Exception as e:
    print("Failed to fetch usernames:", e)
    username_lst = []
    

# Initialize Sense HAT
sense = SenseHat()
sense.clear()

# Push 10 sensor readings to Firebase
for _ in range(10):
    temperature = round(sense.get_temperature(), 2)
    pressure = round(sense.get_pressure(), 2)
    humidity = round(sense.get_humidity(), 2)

    sensorData = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        db.child(username).child(dataset).push(sensorData)
        print(f"Pushed: {sensorData}")
    except Exception as e:
        print("Firebase push failed:", e)

    time.sleep(1)

# Read and print last 3 entries for each teammate
for user in username_lst:
    try:
        mySensorData = db.child(user).child(dataset).get()
    except Exception as e:
        print(f"Failed to fetch data for {user}: {e}")
        continue

    if mySensorData.each() is None:
        continue

    mySensorData_list = mySensorData.each()
    print(f"\nUser: {user}")

    # Print last 3 data points
    for i in range(1, min(4, len(mySensorData_list)+1)):
        lastDataPoint = mySensorData_list[-i]
        print("Child Key: {}".format(lastDataPoint.key()))
        print("Child Value: {}\n".format(lastDataPoint.val()))
