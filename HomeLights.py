import argparse
import json
import pandas as pd
import re
import sys
import time

import merkury

from flask import Flask, jsonify, request, Response
import multiprocessing
import threading
import inspect


app = Flask(__name__)

# ###
# Functions
# ###

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


# ###
# Special Configs
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
    data = data.to_dict()  # convert dataframe to dictionary
    response = jsonify({'data': data})
    return response
    time.sleep(1)
    print(inspect.stack()[0][3]+' fired off successfully')
    
def setDesk():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)
    
    merkury.overheadLight.turn_on()
    merkury.overheadLight.set_value(2, 255)
     
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')
    
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
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(50)
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
    
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
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
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')

# ###
# Stream Configs
# ###
    
def setStream():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(50)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(255, 132, 0)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(0, 157, 255)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(255, 49, 155)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(255, 238, 0)
    time.sleep(0.1)
    
    merkury.overheadLight.turn_on()
    merkury.overheadLight.set_value(2, 125)
    time.sleep(0.1)
     
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')
    
def setZoom():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(50)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(0, 200, 255)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(0, 255, 0)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(0, 200, 255)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(0, 255, 0)
    time.sleep(0.1)
    
    merkury.overheadLight.turn_on()
    merkury.overheadLight.set_value(2, 255)
    time.sleep(0.1)
     
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')

    
def setPlay():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(50)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(255, 132, 0)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(0, 157, 255)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(255, 49, 155)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(255, 238, 0)
    time.sleep(0.1)
    
    merkury.overheadLight.turn_off(switch=0)
    time.sleep(0.1)
     
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')
        
def setRainy():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(50)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(0, 0, 128)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(0, 0, 255)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(0, 0, 128)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(0, 0, 255)
    time.sleep(0.1)
    
    merkury.overheadLight.turn_off(switch=0)
    time.sleep(0.1)
     
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')
    
# ###
# Ambience/Stream Configs
# ###
   
   
# ###
# Destiny 2 Configs
# ###

def setArc():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(0,206,209)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(0,183,235)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(0,206,209)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(0,183,235)
    time.sleep(0.1)
    
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')
    
def setSolar():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(255, 159, 0)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(255, 94, 14)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(255, 159, 0)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(255, 94, 14)
    time.sleep(0.1)
    
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')
    
def setStasis():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(0, 24, 94)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(0, 60, 255)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(0, 24, 94)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(0, 60, 255)
    time.sleep(0.1)
    
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')
    
def setVoid():
    merkury.deskLight.turn_on()
    merkury.deskLight.set_mode('white')
    merkury.deskLight.set_brightness_percentage(25)
    time.sleep(0.1)

    merkury.shelfLight.turn_on()
    merkury.shelfLight.set_mode('colour')    
    merkury.shelfLight.set_colour(75, 0, 130)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_mode('colour')    
    merkury.gameLight.set_colour(143, 0, 255)
    time.sleep(0.1)
    merkury.topShelfLight.turn_on()
    merkury.topShelfLight.set_mode('colour')    
    merkury.topShelfLight.set_colour(75, 0, 130)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_mode('colour')    
    merkury.letterLight.set_colour(143, 0, 255)
    time.sleep(0.1)
    
    time.sleep(0.4)    
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+' fired off successfully')


# ###
# Twitch Functions
# ###

def setTwitchalert(modal):
    
    duration = {'follow':10, 'sub':15, 'cheer':15, 'host':15, 'raid':30, 'donation':20}
    
    merkury.deskLight.turn_on()
    merkury.deskLight.set_scene(4)
    time.sleep(0.1)
    merkury.gameLight.turn_on()
    merkury.gameLight.set_scene(4)
    time.sleep(0.1)
    merkury.letterLight.turn_on()
    merkury.letterLight.set_scene(4)
    
    time.sleep(duration[modal])
    
    merkury.gameLight.set_mode('colour')
    time.sleep(0.1)
    merkury.letterLight.set_mode('colour')
    time.sleep(0.1)
    merkury.deskLight.set_mode('colour')
    time.sleep(0.5)
    print(inspect.stack()[0][3]+'('+modal+') fired off successfully')

def setChatalert(userHexColor):
    print('Trying to change light to '+userHexColor)
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
    command = request.args.get("command")
    subCommand = request.args.get("effect")
    q.put([command,subCommand])
    return Response()

def handler(command_queue):
    while True:
        command = command_queue.get() # blocking call
        if command[1] is not None:
            eval("set"+command[0].capitalize()+"('"+command[1]+"')")
        else:
            eval('set'+command[0].capitalize()+'()') 
    

# ###
# Program Start
# ###

if __name__ == "__main__":
    print('Home Lights Starting') 
    
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=handler, args=((q),))

    p.start()

    app.run(host='0.0.0.0', port=64250)

    p.join()
    
    print('Home Lights Server Started') 
   


