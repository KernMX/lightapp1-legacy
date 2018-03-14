'''
Steps for adding a new pattern:
1. Create new animation function using the template
2. Add the new animation function to the setPattern switch statement
3. Increase the shufflePattern() function's randint by 1
'''

'''
Animation Function Template:
def Function():
    global animation
    animation = Function
    #send udp string
    MESSAGE = "Function"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
'''

#import led
import config
import visualization
import microphone

#import other
import colorsys
import time
import threading
import socket
import random


################################ GLOBAL VARIABLES #########################################
lastShuffle = 0
shuffleDuration = 10.0
shufflingV = False
wasShufflingV = False
shuffler = threading.Timer(1.0, print)
shuffler.daemon = True
UDP_IP = config.UDP_IP
UDP_PORT = config.UDP_PORT
currentVis = ""
currentColor = {"r": 255, "g":255, "b":255}
isRunning = False



################################ POWER CONROLS #########################################
def on():
    print("animation on")
    animation()

def off():
    print("animation off")
    global animation
    global wasShufflingV
    if animation == visualize:
        if shufflingV:
            wasShufflingV = True
        stop()
    elif animation == startShufflePattern:
        stopShuffle()
    MESSAGE = "off"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))



################################ SLIDER CONTROLS #########################################
def setBrightness(brightness):
    print("animation brightnes")
    print(brightness)
    MESSAGE = 'brightness {}'.format(brightness)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def setSpeed(speed):
    print("animation Speed")
    print(speed)
    speedMap = {1:15, 2:30, 3:60, 4:120, 5:240, 6:480}
    MESSAGE = 'speed {}'.format(speedMap[speed])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))



################################ PATTERN ANIMATIONS #########################################
def setPattern(pattern):
    patternString = ""
    if animation == visualize:
        stop()
    if pattern == 0:
        patternString = "Shuffle"
        startShufflePattern()
    elif pattern == 1:
        patternString = "Flash"
        flash()
    elif pattern == 2:
        patternString = "Fade"
        fade()
    elif pattern == 3:
        patternString = "Rainbow"
        rainbow()
    elif pattern == 4:
        patternString = "Rainbow With Glitter"
        rainbowWithGlitter()
    elif pattern == 5:
        patternString = "Cylon"
        cylon()
    elif pattern == 6:
        patternString = "Sinelon"
        sinelon()
    elif pattern == 7:
        patternString = "Confetti"
        confetti()
    elif pattern == 8:
        patternString = "BPM"
        bpm()
    elif pattern == 9:
        patternString = "Juggle"
        juggle()
    else:
        patternString = "Error Not a Pattern"
    print(patternString)
    return patternString

def shufflePattern():
    global lastShuffle
    global shuffler
    global animation
    if animation != startShufflePattern:
        stopShuffle()
        return
    newShuffle = random.randint(1,9)
    while(lastShuffle == newShuffle):
        newShuffle = random.randint(1,9)
    lastShuffle = newShuffle
    setPattern(newShuffle)
    animation = startShufflePattern
    shuffler = threading.Timer(shuffleDuration, shufflePattern)
    shuffler.daemon = True
    shuffler.start()

def startShufflePattern():
    stopShuffle()
    global animation
    animation = startShufflePattern
    shufflePattern()

def stopShuffle():
    global shuffler
    global shufflingV
    shuffler.cancel()
    shufflingV = False

def flash():
    global animation
    animation = flash
    #send udp string
    MESSAGE = "flash"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def fade():
    global animation
    animation = fade
    #send udp string
    MESSAGE = "fade"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def rainbow():
    global animation
    animation = rainbow
    #send udp string
    MESSAGE = "rainbow"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def rainbowWithGlitter():
    global animation
    animation = rainbowWithGlitter
    #send udp string
    MESSAGE = "rainbowWithGlitter"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def cylon():
    global animation
    animation = cylon
    #send udp string
    MESSAGE = "cylon"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def sinelon():
    global animation
    animation = sinelon
    #send udp string
    MESSAGE = "sinelon"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def confetti():
    global animation
    animation = confetti
    #send udp string
    MESSAGE = "confetti"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def bpm():
    global animation
    animation = bpm
    #send udp string
    MESSAGE = "bpm"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def juggle():
    global animation
    animation = juggle
    #send udp string
    MESSAGE = "juggle"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))



################################ VISUALIZATION ANIMATIONS #########################################
def setVisualization(visualization):
    global currentVis
    global wasShufflingV
    visualizationString = ""
    if visualization == 0:
        visualizationString = "Shuffle"
        startShuffleVisualization()
    elif visualization == 1:
        visualizationString = "Energy"
        currentVis = "energy"
        stopShuffle()
        wasShufflingV = False
        visualize()
    elif visualization == 2:
        visualizationString = "Spectrum"
        currentVis = "spectrum"
        stopShuffle()
        wasShufflingV = False
        visualize()
    elif visualization == 3:
        visualizationString = "Scroll"
        currentVis = "scroll"
        stopShuffle()
        wasShufflingV = False
        visualize()
    else:
        stopShuffle()
        visualizationString = "Error Not a Visualization"
    print(visualizationString)
    return visualizationString

def stop():
    print("Stopping")
    microphone.running = False
    stopShuffle()
    time.sleep(.01)

def shuffleVisualization():
    global lastShuffle
    global shuffler
    global currentVis
    if not shufflingV:
        stopShuffle()
        return
    newShuffle = random.randint(1,3)
    while(lastShuffle == newShuffle):
        newShuffle = random.randint(1,3)
    lastShuffle = newShuffle
    if newShuffle == 1:
        currentVis = "energy"
    elif newShuffle == 2:
        currentVis = "spectrum"
    else:
        currentVis = "scroll"
    visualize()
    shuffler = threading.Timer(shuffleDuration, shuffleVisualization)
    shuffler.daemon = True
    shuffler.start()

def startShuffleVisualization():
    stopShuffle()
    global animation
    global shufflingV
    shufflingV = True
    animation = visualize
    shuffleVisualization()


def visualize():
    global currentVis
    global animation
    global wasShufflingV
    if(not microphone.running):
        animation = juggle
    if wasShufflingV:
        wasShufflingV = False
        startShuffleVisualization()
        return
    if currentVis == "scroll":
        scrollMusic()
    elif currentVis == "spectrum":
        spectrumMusic()
    else:
        energyMusic()

def energyMusic():
    global animation
    global isRunning
    if animation != visualize:
        MESSAGE = "visualize"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        isRunning = False
    animation = visualize
    visualization.visualization_effect = visualization.visualize_energy
    if not isRunning:
        isRunning = True;
        print('now running')
        t = threading.Thread(target=microphone.start_stream, args=[visualization.microphone_update])
        t.daemon = True
        t.start()


def scrollMusic():
    global animation
    global isRunning
    if animation != visualize:
        MESSAGE = "visualize"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        isRunning = False
    animation = visualize
    visualization.visualization_effect = visualization.visualize_scroll
    if not isRunning:
        isRunning = True;
        print('now running')
        t = threading.Thread(target=microphone.start_stream, args=[visualization.microphone_update])
        t.daemon = True
        t.start()

def spectrumMusic():
    global animation
    global isRunning
    if animation != visualize:
        isRunning = False
        MESSAGE = "visualize"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    animation = visualize
    visualization.visualization_effect = visualization.visualize_spectrum
    if not isRunning:
        isRunning = True;
        print('now running')
        t = threading.Thread(target=microphone.start_stream, args=[visualization.microphone_update])
        t.daemon = True
        t.start()

################################ COLOR ANIMATIONS #########################################
def staticRGB(r, g, b):
    print('animation color')
    print(r,g,b)
    global animation
    global currentColor
    currentColor["r"] = r
    currentColor["g"] = g
    currentColor["b"] = b
    if animation == visualize:
        stop()
    animation = setColor
    MESSAGE = 'static {} {} {}'.format(r, g, b)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

def setColor():
    global currentColor
    staticRGB(currentColor["r"], currentColor["g"], currentColor["b"])



################################ ANIMATION GLOBAL #########################################
animation = juggle
