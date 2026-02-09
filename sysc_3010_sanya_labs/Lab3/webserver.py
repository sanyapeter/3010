# Importing modules
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sense_hat import SenseHat
import json

# Initialization of RGB colors
colors = [[10, 10, 10] for i in range(64)]

# Creates a Flask web application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Attach SocketIO to the Flask app for real-time communication
socketio = SocketIO(app)

# Initialize the SenseHAT
sense = SenseHat()

# Converts a HEX color string to an RGB list
def hex_to_rgb_color(color: str):
    color = color.strip('#')
    rgb = [int(color[i:i+2], 16) for i in (0, 2, 4)]
    return rgb

# Map LED index to x, y coordinates on SenseHAT
def map_index_to_xy(led_index: int):
    return int(led_index % 8), int(led_index / 8)

@app.route('/')
def index():
    return render_template('Lab3-Colour-Picker.html')

# Send current LED colors to newly connected clients
@socketio.on('connect')
def send_led_colors():
    print(f"sending colors.. {json.dumps({'colors': colors})}")
    emit('current_colors', json.dumps({'colors': colors}))

# Update the physical SenseHAT LEDs
def update_sensehat_leds():
    for index, color in enumerate(colors):
        x, y = map_index_to_xy(index)
        sense.set_pixel(x, y, color[0], color[1], color[2])

# Update a specific LED when a client changes it
@socketio.on('update_led')
def update_led_color(data):
    data = json.loads(data)
    color_rgb = hex_to_rgb_color(data['color'])
    colors[int(data['id'])] = color_rgb
    # Broadcast the update to all clients
    emit('update_led', json.dumps({'id': data['id'], 'color': data['color']}), broadcast=True)
    # Update the SenseHAT
    update_sensehat_leds()

# Clear all LEDs when requested by a client
@socketio.on('clear_leds')
def clear_leds():
    # Reset colors array
    for i in range(64):
        colors[i] = [0, 0, 0]
    # Update SenseHAT LEDs
    update_sensehat_leds()
    # Broadcast cleared colors to all clients
    emit('current_colors', json.dumps({'colors': colors}), broadcast=True)

if __name__ == '__main__':
    # Run the Flask app with SocketIO support
    socketio.run(app, host="0.0.0.0", debug=True)
