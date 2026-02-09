from sense_hat import SenseHat
sense = SenseHat()

while True:
    temp = sense.get_temperature()
    pressure = sense.get_pressure()
    humid = sense.get_humidity()
    
    temp = round(temp,2)
    pressure = round(pressure,2)
    humid = round(humid,2)
    message = "Temperature: " + str(temp) + " Pressure: " + str(pressure) + " Humidity: " + str(humid)
    sense.show_message(message, scroll_speed=0.05)
