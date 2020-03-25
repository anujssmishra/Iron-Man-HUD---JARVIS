# -*- coding: utf-8 -*-

import cv2
import numpy as np
from pygame import mixer
from PIL import ImageFont, ImageDraw, Image
# import weather
import psutil
import datetime



def addText(added_image, x,level_str):
    cpu = int(psutil.cpu_percent())
    fontpath = "./good times rg.ttf"     
    font = ImageFont.truetype(fontpath, 22)
    img_pil = Image.fromarray(added_image)
    draw = ImageDraw.Draw(img_pil)

    # Date, Time and Day
    a = datetime.datetime.now()
    draw.text((120,660),  a.strftime("%H")+" : "+a.strftime("%M"), font = ImageFont.truetype(fontpath, 48), fill = (168,98,0,0)) # Hour and Minute
    draw.text((325,684),  a.strftime("%S"), font = ImageFont.truetype(fontpath, 24), fill = (168,98,0,0)) # Seconds
    draw.text((135,725),  a.strftime("%A"), font = ImageFont.truetype(fontpath, 24), fill = (168,98,0,0)) # Day
    draw.text((127,760),  a.strftime("%d")+"  "+a.strftime("%b"), font = ImageFont.truetype(fontpath, 40), fill = (168,98,0,0)) # Date and Month
    draw.text((175,800),  a.strftime("%Y"), font = ImageFont.truetype(fontpath, 36), fill = (168,98,0,0)) # Year

    # Getting Battery info
    with open('/sys/class/power_supply/BAT1/charge_now', 'r') as f:
        current = f.read()
    with open('/sys/class/power_supply/BAT1/charge_full', 'r') as f:
        full = f.read()
    battery = int(int(current)*100/int(full))

    # Battery level
    global count
    if count==0:
        if x<1270:
            if x%20!=0:
                level_str = level_str.join("| ")
            else:
                level_str = level_str.join("| ")
                level_str = level_str.join("| ")
        else:
            level_str = level_str[:191]
            count = 1
    else:
        level_str = level_str[0:int(battery*191/100.0)]
    draw.text((0,0),  level_str, font = ImageFont.truetype(fontpath, 34), fill = (168,98,0,0))

    # Battery percentage
    draw.text((130,430),  "BATTERY", font = ImageFont.truetype(fontpath, 18), fill = (168,98,0,0))
    if battery==100:
        draw.text((157,505),  str(battery), font = ImageFont.truetype(fontpath, 24), fill = (255,201,125,0))
    elif battery<10:
        draw.text((162,493),  str(battery), font = ImageFont.truetype(fontpath, 42), fill = (255,201,125,0))
    elif battery<20:
        draw.text((162,500),  str(battery), font = ImageFont.truetype(fontpath, 32), fill = (255,201,125,0))
    else:
        draw.text((155,500),  str(battery), font = ImageFont.truetype(fontpath, 30), fill = (255,201,125,0))

    # Weather
    # draw.text((1300, 185),  weather.sky, font = font, fill = (168,98,0,0))
    # draw.text((1467, 275),  str(weather.temperature)+'°', font = ImageFont.truetype(fontpath, 48), fill = (255,201,125,0))
    
    # CPU Usage
    draw.text((90, 150),  "CPU  USAGE", font = ImageFont.truetype(fontpath, 24), fill = (255,201,125,0))
    draw.text((135, 175),  str(cpu), font = ImageFont.truetype(fontpath, 54), fill = (255,201,125,0))

    added_image = np.array(img_pil)
    return added_image, x+10, level_str


# create an overlay image. You can use any image
foreground = cv2.imread('JARVIS2.png')
foreground = cv2.resize(foreground, (1920,1080))
# Open the camera
# cap = cv2.VideoCapture('http://192.168.0.102:8080/video')
cap = cv2.VideoCapture(0)
# Set initial value of weights)
alpha = 0.4
mixer.init()
mixer.music.load('jarvis_sound.mp3')
mixer.music.play()
x = 0
count=0
level_str = ""
while True:
    # read the background
    ret, background = cap.read()
    background = cv2.flip(background,1)
    background = cv2.resize(background, (1920,1080))
    
    # Select the region in the background where we want to add the image and add the images using cv2.addWeighted()
    added_image = cv2.addWeighted(background,1,foreground,1,0)

    # Add Text
    added_image, x,level_str = addText(added_image, x,level_str)

    # Change the region with the result
    cv2.imshow('frame1',added_image)
    k = cv2.waitKey(10)
    # Press q to break
    if k == ord('q'):
        break
# Release the camera and destroy all windows         
cap.release()
cv2.destroyAllWindows()