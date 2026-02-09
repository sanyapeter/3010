from gpiozero import LED

class TrafficLights:
    def __init__(self, red_led, yellow_led, green_led):
        """Initialize the TrafficLights with three GPIO pins."""
        self.red_led = LED(red_led)
        self.yellow_led = LED(yellow_led)
        self.green_led = LED(green_led)
        
    def red(self):
        """Turn on the red light and turn off the others."""
        self.red_led.on()
        self.yellow_led.off()
        self.green_led.off()

    def yellow(self):
        """Turn on the yellow light and turn off the others."""
        self.red_led.off()
        self.yellow_led.on()
        self.green_led.off()
        
    def green(self):
        """Turn on the green light and turn off the others."""
        self.red_led.off()
        self.yellow_led.off()
        self.green_led.on()
