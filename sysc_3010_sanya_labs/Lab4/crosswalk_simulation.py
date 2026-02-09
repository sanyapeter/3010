from gpiozero import LED, Button
from time import sleep, time

# GPIO pins
RED_LED = 12
YELLOW_LED = 13
GREEN_LED = 26
#BUTTON_PIN = 21

# Setup LEDs and button
red = LED(RED_LED)
yellow = LED(YELLOW_LED)
green = LED(GREEN_LED)
button = Button(BUTTON_PIN)

def traffic_cycle():
    """Continuous traffic light cycle with button support."""
    while True:
        # RED light
        red.on()
        yellow.off()
        green.off()
        print("Red Light - Cars Stop")
        sleep(5)

        # GREEN light
        red.off()
        green.on()
        yellow.off()
        print("Green Light - Cars Go")
        start = time()
        while time() - start < 5:  # Green lasts 5 seconds
            if button.is_pressed:
                print("Pedestrian button pressed! Switching to yellow early...")
                sleep(1)  # brief pause before yellow
                break
            sleep(0.1)

        # YELLOW light
        green.off()
        yellow.on()
        red.off()
        print("Yellow Light - Get Ready to Stop")
        sleep(2)
        yellow.off()  # turn off yellow before next cycle

try:
    traffic_cycle()
except KeyboardInterrupt:
    print("\nSimulation stopped by user.")
    # Turn off all LEDs safely
    red.off()
    yellow.off()
    green.off()
