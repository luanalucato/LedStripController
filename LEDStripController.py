
import time
from rpi_ws281x import *
import argparse
from flask import Flask

import _thread
import time
from flask import request

app = Flask(__name__)


LED_COUNT      = 600      
LED_PIN        = 18      
#LED_PIN        = 10      
LED_FREQ_HZ    = 800000  
LED_DMA        = 10      
LED_BRIGHTNESS = 255     
LED_INVERT     = False   

def send_color(threadName, strip, color):
    
    colorWipe(strip, color)  

@app.route('/')
def hello():
    _thread.start_new_thread( send_color , ("Thread-1", strip,Color(), ))  
    return "Hello World!"


def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        if(i - 30 > 0):
            strip.setPixelColor(i - 30, Color(0,0,0)) 
        
        strip.show()
    for i in range(strip.numPixels() - 30, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        time.sleep(wait_ms/30000.0)
        strip.show()

@app.route('/green')
def green():
    _thread.start_new_thread( send_color , ("Thread-1", strip,Color(155,105,180), ))  
    return "Hello World!"

@app.route('/blue')
def blue():
    _thread.start_new_thread( send_color , ("Thread-1", strip,Color(128, 206, 225), ))  
    return "Hello World!"

@app.route('/red')
def red():
    send_color("Thread-1", strip,Color(155,105,180))

    return "Hello World!"

@app.route('/chooseColor', methods=['POST'])
def chooseColor():
    red = request.form["red"]
    green = request.form['green']
    blue = request.form['blue']
    print(red, " " , green , " " , " " , blue)
    ChangeAllLEDToColor(strip, red, green, blue)
    return "true"

@app.route("/test", methods=["POST"])
def test():
    print(request.form["red"])
    return "true"

def ChangeAllLEDToColor(strip, red, green, blue):
    print("Changing colors")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(int(red), int(green), int(blue)))
    strip.show()


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    
    strip.begin()

    app.run(host='0.0.0.0')