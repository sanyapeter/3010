from traffic_lights import TrafficLights

# Define GPIO pins
RED_LED = 12
YELLOW_LED = 13
GREEN_LED = 26

# Create traffic light instance
traffic_lights = TrafficLights(RED_LED, YELLOW_LED, GREEN_LED)

# Test red
traffic_lights.red()
assert traffic_lights.red_led.is_lit
assert not traffic_lights.yellow_led.is_lit
assert not traffic_lights.green_led.is_lit

# Test yellow
traffic_lights.yellow()
assert not traffic_lights.red_led.is_lit
assert traffic_lights.yellow_led.is_lit
assert not traffic_lights.green_led.is_lit

# Test green
traffic_lights.green()
assert not traffic_lights.red_led.is_lit
assert not traffic_lights.yellow_led.is_lit
assert traffic_lights.green_led.is_lit

print("All tests passed successfully")
