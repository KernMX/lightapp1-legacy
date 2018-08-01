#webapp imports
from flask import Flask, render_template, json
from flask_socketio import SocketIO, emit
#pip install eventlet
#pip install flask-socketio

#led control imports
import sys
sys.path.insert(0,'visualization')
import animation

#initializing app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

#State Variables
patterns = ["Shuffle", "Flash", "Fade", "Rainbow", "Rainbow With Glitter", "Cylon", "Sinelon", "Confetti", "BPM", "Juggle"]
visualizations = ["Shuffle", "Energy", "Spectrum", "Scroll"]
state = {
    "power" : 0,
    "brightness" : 50,
    "speed" : 4,
    "patterns" : patterns,
    "pattern": 0,
    "visualizations" : visualizations,
    "visualization" : 0,
    "color": {
    "r" : 255,
    "g" : 255,
    "b" : 255
    },
}

@app.route('/')
def homepage():
    return render_template("index.html")

@socketio.on('connect') #when a client is connected
def connectClient():
    print('Client Connected\n')

@socketio.on('getState') #when a client is connected
def getState():
    print('Getting State\n')
    return json.dumps(state)

@socketio.on('setPower')
def setPower(power):
    print('setting Power')
    state['power'] = power #Set this after MQTT responds with OK
    socketio.emit('updatePower', power, broadcast=True) #same as above
    if power:
        animation.on()
    else:
        animation.off()
    #Call to MQTT

@socketio.on('setBrightness')
def setBrightness(brightness):
    print('setting Brightness')
    state['brightness'] = brightness #Set this after MQTT responds with OK
    socketio.emit('updateBrightness', brightness, broadcast=True) #same as above
    animation.setBrightness(int(brightness))
    #Call to MQTT

@socketio.on('setSpeed')
def setSpeed(speed):
    print('setting Speed')
    state['speed'] = speed #Set this after MQTT responds with OK
    animation.setSpeed(int(speed))
    socketio.emit('updateSpeed', speed, broadcast=True) #same as above
    #Call to MQTT

@socketio.on('setPattern')
def setPattern(pattern):
    print('setting Pattern')
    state['pattern'] = pattern #Set this after MQTT responds with OK
    state['visualization'] = 0
    state['color']['r'] = 255
    state['color']['g'] = 255
    state['color']['b'] = 255
    data = {'pattern': state['pattern'], 'visualization': state['visualization'], 'color': state['color']}
    socketio.emit('updatePattern', json.dumps(data), broadcast=True) #same as above
    animation.setPattern(int(pattern) - 1)
    #Call to MQTT

@socketio.on('setVisualization')
def setVisualization(visualization):
    print('setting Visualization')
    state['pattern'] = 0 #Set this after MQTT responds with OK
    state['visualization'] = visualization
    state['color']['r'] = 255
    state['color']['g'] = 255
    state['color']['b'] = 255
    data = {'pattern': state['pattern'], 'visualization': state['visualization'], 'color': state['color']}
    socketio.emit('updateVisualization', json.dumps(data), broadcast=True) #same as above
    animation.setVisualization(int(visualization) - 1)
    #Call to MQTT

@socketio.on('setColor')
def setColor(color):
    print('setting Color')
    state['pattern'] = 0 #Set this after MQTT responds with OK
    state['visualization'] = 0
    state['color']['r'] = color['r']
    state['color']['g'] = color['g']
    state['color']['b'] = color['b']
    data = {'pattern': state['pattern'], 'visualization': state['visualization'], 'color': state['color']}
    socketio.emit('updateVisualization', json.dumps(data), broadcast=True) #same as above
    animation.staticRGB(int(color['r']), int(color['g']), int(color['b']))
    #Call to MQTT

@socketio.on('disconnect') #when a client is disconnected
def disconnectClient():
    print('Client disconnected\n')


if __name__ == '__main__':
    print('Starting Server')
    socketio.run(app, host='localhost', port=5000, debug=False)
