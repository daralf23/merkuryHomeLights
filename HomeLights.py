import argparse
import inspect
import json
import multiprocessing
import pandas as pd
import random
import re
import sys
import threading
import time

from flask import Flask, jsonify, request, Response
app = Flask(__name__)

import merkury


# ###
# Functions
# ###

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


# ###
# Home Functions
# ###

def getInfo():
    merkury.deskLight.turn_off()
    time.sleep(0.1)
    infoDeskLight = "Desk Light - "+json.dumps(merkury.deskLight.status())
    time.sleep(0.1)
    infoShelfLight = "Shelf Light - "+json.dumps(merkury.shelfLight.status())
    time.sleep(0.1)
    infoTopShelfLight = "Top Shelf Light - "+json.dumps(merkury.topShelfLight.status())
    time.sleep(0.1)
    infoGameLight = "Top Shelf Light - "+json.dumps(merkury.gameLight.status())
    time.sleep(0.1)
    infoOverheadLight = "Overhead Light - "+json.dumps(merkury.overheadLight.status())
    time.sleep(0.1)
    infoLetterLight = "Letter Light - "+json.dumps(merkury.letterLight.status())
    time.sleep(0.4)
    merkury.deskLight.turn_on()
    
    data = pd.DataFrame([infoDeskLight,infoShelfLight, infoTopShelfLight, infoGameLight, infoOverheadLight, infoLetterLight], columns=['LightInfo'])
    response = jsonify({'data': data.to_dict()})
    return response
    

def setEffect(modal):
    if modal == 'off':
        setOff()
    elif modal == 'rainbow':
        setRainbow()
    elif modal == 'study':
        setStudy()


def setOff():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)

    merkury.shelfLight.turn_off()
    time.sleep(0.1)
    merkury.gameLight.turn_off()
    time.sleep(0.1)
    merkury.topShelfLight.turn_off()
    time.sleep(0.1)
    merkury.letterLight.turn_off()
    time.sleep(0.1)
    
    merkury.overheadLight.turn_off()
    time.sleep(0.1)
     
    time.sleep(0.4)    
    merkury.deskLight.turn_off()
    time.sleep(1)
    print(inspect.stack()[0][3]+' fired off successfully')


def setRainbow():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_scene(4)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_scene(4)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_scene(4)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode(mode='scene')
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode(mode='scene')
    time.sleep(0.1)
    
    print(inspect.stack()[0][3]+' fired off successfully')


def setStudy():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(50)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('white')    
    merkury.shelfLight.set_brightness_percentage(75)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('white')    
    merkury.gameLight.set_brightness_percentage(75)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('white')    
    merkury.topShelfLight.set_brightness_percentage(75)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('white')    
    merkury.letterLight.set_brightness_percentage(75)
    time.sleep(0.1)
    
    merkury.overheadLight.turn_on()
    merkury.overheadLight.set_value(2, 255)
    time.sleep(0.1)
     
    time.sleep(0.4)    
    merkury.deskLight.set_brightness_percentage(75)
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')


def setDeskLight(modal):
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)

    if modal == 'on':
        merkury.overheadLight.turn_on()
        merkury.overheadLight.set_value(2, 255)

        time.sleep(0.4)          
        merkury.deskLight.set_brightness_percentage(50)
    else:
        merkury.overheadLight.turn_off(switch=0)
        time.sleep(0.4)    
        merkury.deskLight.set_mode('colour')    

    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')


def setCustomColors(colorDict):
    numColors = len(colorDict)
    
    colorList = list(colorDict.values())
    random.shuffle(colorList)

    if numColors < 1:
        return
    elif numColors == 1:
        r1, g1, b1 = hex_to_rgb(colorList[0])
        r2, r3, r4, g2, g3, g4, b2, b3, b4 = r1, r1, r1, g1, g1, g1, b1, b1, b1
    elif numColors ==2:
        r1, g1, b1 = hex_to_rgb(colorList[0])
        r2, g2, b2 = hex_to_rgb(colorList[1])
        r3, g3, b3 = r1, g1, b1
        r4, g4, b4 = r2, g2, b2
    elif numColors ==3:
        r1, g1, b1 = hex_to_rgb(colorList[0])
        r2, g2, b2 = hex_to_rgb(colorList[1])
        r3, g3, b3 = hex_to_rgb(colorList[2])
        r4, g4, b4 = r2, g2, b2
    elif numColors <=4:
        r1, g1, b1 = hex_to_rgb(colorList[0])
        r2, g2, b2 = hex_to_rgb(colorList[1])
        r3, g3, b3 = hex_to_rgb(colorList[2])
        r4, g4, b4 = hex_to_rgb(colorList[3])    

    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(r1, g1, b1)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(r2, g2, b2)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(r3, g3, b3)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(r4, g4, b4)
    time.sleep(0.1)
    
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully') 


# ###
# Twitch Functions
# ###

def setTwitchalert(modal):
    duration = {'follow':10, 'sub':15, 'cheer':15, 'host':15, 'raid':20, 'donation':30}
    
    merkury.deskLight.turn_on()
    merkury.deskLight.set_scene(4)
    time.sleep(0.1)
    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_scene(4)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_scene(4)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode(mode='scene')
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode(mode='scene')
    time.sleep(0.1)

    time.sleep(duration[modal])
    
    merkury.shelfLight.set_mode('colour')
    time.sleep(0.1)
    merkury.gameLight.set_mode('colour')
    time.sleep(0.1)
    merkury.topShelfLight.set_mode('colour')
    time.sleep(0.1)
    merkury.letterLight.set_mode('colour')
    time.sleep(0.1)
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+'('+modal+') fired off successfully')


def setChatalert(userHexColor):
    r, g, b = hex_to_rgb(userHexColor)
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)

    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(r, g, b)
    time.sleep(0.1)
     
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(r, g, b)
    time.sleep(0.1)

    time.sleep(0.2)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+'('+userHexColor+') fired off successfully')


# ###
# Web Hooks and Queue Handling
# ###
  
@app.route('/lightInfo', methods = ['GET'])
def lightsInfo():
    return getInfo()

@app.route("/lights", methods=["POST"])
def lightEndPoint():
    jsonCommand = request.get_json()
    q.put(jsonCommand)
    return 'Command Queued'

def handler(command_queue):
    while True:
        command = command_queue.get() # blocking call
        if "effect" in command: # Tested
            print(command['effect']+' was triggered')
            setEffect(command['effect'])
        elif "hexcodes" in command: # Dev
            print(command['hexcodes'])
            setCustomColors(command['hexcodes'])
        elif "twitch" in command: # Tested
            print(command['twitch']+' was triggered')
            setTwitchalert(command['twitch'])
        elif "desk" in command: # Tested
            print('Desk was triggered')
            setDeskLight(command['desk'])
        elif "chat" in command: # Ready for Testing
            print('Chat was triggered')
            setChatalert(command['chat'])
        else:
            print('Unidentified Command')        
    

# ###
# Program Start
# ###

if __name__ == "__main__":
    print('Test Lights Starting') 
    
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=handler, args=((q),))
    p.start()
    app.debug = True
    app.run(host='0.0.0.0', port=64251)
    p.join()