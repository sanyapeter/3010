# Lab 3 – Pyrebase example code 
import pyrebase
from sense_hat import SenseHat
from datetime import datetime
import time
import os
import json

# Load Firebase configuration securely from environment variable
config = json.loads(os.environ['W24SYSC3010LAB3FIREBASECONFIG'])

# Config will contain the information needed to connect to your firebase 
#   The API KEY and Project ID are found in your project settings 
#   The DB URL can be found under the Realtime Database tab 
config = { 
  "apiKey": "AIzaSyC2D_7aOU2d_OK88ExLGT6Qs6QqduK-LTs", 
  "authDomain": "sysc3010-ed257.firebaseapp.com", 
  "databaseURL": "https://sysc3010-ed257-default-rtdb.firebaseio.com/", 
  "storageBucket": "sysc3010-ed257.appspot.com" 
} 

# Connect using your configuration 
firebase = pyrebase.initialize_app(config) 
db = firebase.database() 
dataset = "sensor1" 
username = "sanya" 

username_lst = [
    "sanya",
    "Sydney",
    "Sahand",
    "Ryan",
    "Jad"
]

sense = SenseHat()
sense.clear()

# Write 10 data entries to the DB in a loop 
key = 0 
while(key < 10): 
    temperature = sense.get_temperature()
    pressure = sense.get_pressure()
    humidity = sense.get_humidity()

    # rounding values to two decimal places 
    temperature = round(temperature, 2)
    pressure = round(pressure, 2)
    humidity = round(humidity, 2)
    
    # store sensor data as a dictionary instead of a string
    sensorData = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
  
    # When writing to your DB each child is a JSON key:value pair 
    db.child(username).child(dataset).child(str(key)).set(sensorData) 

    # Increment the key and loop 
    key += 1 
    time.sleep(1)  # optional: wait 1 second between readings

# Next, we will retrieve the data we wrote to the DB 
# This code will read all sensor data as a Python dictionary, 
# convert it to a list, extract the final entry, and print its  
# key and value pair 

for user in username_lst:
    mySensorData = db.child(user).child(dataset).get() 

    # Returns the dictionary as a list 
    mySensorData_list = mySensorData.each() 

    if mySensorData_list is None:
        continue

    print("User:", user)

    for i in range(1, 4):
        lastDataPoint = mySensorData_list[-i] 
        print("Child Key: {}".format(lastDataPoint.key())) 
        print("Child Value: {}\n".format(lastDataPoint.val()))
