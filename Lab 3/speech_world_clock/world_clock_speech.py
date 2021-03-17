import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from datetime import datetime
import pytz 
from random import randint
import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from i2c_button import I2C_Button

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json
import subprocess
time_zone_name = {
            "-12":"New Zealand\nStandard Time",
            "-11":"Solomon\nStandard Time",
            "-10":"Australia\nEastern Time",
            "-9":"Japan\nStandard Time",
            "-8":"China Taiwan\nTime",
            "-7":"Vietnam\nStandard Time",
            "-6":"Bangladesh\nStandard Time",
            "-5":"Pakistan\nLahore Time",
            "-4":"Near East\nTime",
            "-3":"Eastern African\nTime",
            "-2":"Egypt\nStandard Time",
            "-1":"European\nCentral Time",
            "0":"Greenwich\nMean Time",
            "1":"Central\nAfrican Time",
            "2":"Fernando de\nNoronha Time",
            "3":"Argentina\nStandard Time",
            "4":"Puerto Rico\nTime",
            "5":"Eastern\nStandard Time",
            "6":"Central\nStandard Time",
            "7":"Phoenix\nStandard Time",
            "8":"Pacific\nStandard Time",
            "9":"Alaska\nStandard Time",
            "10":"Hawaii\nStandard Time",
            "11":"Midway\nIslands Time",
            }

time_zone_gmt = {
            "-12":"Etc/GMT-12",
            "-11":"Etc/GMT-11",
            "-10":"Etc/GMT-10",
            "-9":"Etc/GMT-9",
            "-8":"Etc/GMT-8",
            "-7":"Etc/GMT-7",
            "-6":"Etc/GMT-6",
            "-5":"Etc/GMT-5",
            "-4":"Etc/GMT-4",
            "-3":"Etc/GMT-3",
            "-2":"Etc/GMT-2",
            "-1":"Etc/GMT-1",
            "0":"Etc/GMT0",
            "1":"Etc/GMT+1",         
            "2":"Etc/GMT+2",
            "3":"Etc/GMT+3",
            "4":"Etc/GMT+4",
            "5":"Etc/GMT+5",
            "6":"Etc/GMT+6",
            "7":"Etc/GMT+7",
            "8":"Etc/GMT+8",
            "9":"Etc/GMT+9",
            "10":"Etc/GMT+10",
            "11":"Etc/GMT+11",
}


current_tz = 5
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

def Speech2Text():
    wf = wave.open("recording.wav", "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    model = Model("model")
    # You can also specify the possible word list
    rec = KaldiRecognizer(model, wf.getframerate(), "east west day night shanghai paris newyork")

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
    res = json.loads(rec.FinalResult())
    print ("Speech2Text: "+ res['text'])
    return res['text']

def ScaleImage(image):
# Scale the image to the smaller screen dimension
	width = 135
	height = 240

	image_ratio = image.width / image.height
	screen_ratio = width / height
	if screen_ratio < image_ratio:
	    scaled_width = image.width * height // image.height
	    scaled_height = height
	else:
	    scaled_width = width
	    scaled_height = image.height * width // image.width
	image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

	# Crop and center the image
	x = scaled_width // 2 - width // 2
	y = scaled_height // 2 - height // 2
	image = image.crop((x, y, x + width, y + height))

	image = image.convert('RGB')
	image = image.resize((240, 135),Image.BICUBIC)
	return image


if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

# Try to create an I2C device
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")
# ids = '\n'.join(map(str,i2c.scan()))
# print(f"I2C device ID's found:\n{ids}")
 
while not i2c.try_lock():
    pass
 
print("I2C addresses found:", [hex(device_address) for device_address in i2c.scan()])
i2c.unlock()

# initialize the button
button = I2C_Button(i2c)
button.led_bright = 0
button.led_gran = 1
button.led_cycle_ms = 0
button.led_off_ms = 0
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
prevA = True
prevB = True
DAYNIGHTFORCE = False
prevButton = False
speechInput = False
prev_tz = current_tz
while True:
    button.clear()
    time.sleep(1)

    if button.status.is_pressed:
        button.led_bright = 100
        if not prevButton:
            process = subprocess.Popen(["arecord", "-D", "hw:2,0", "-d", "5", "-f", "cd", "recording.wav", "-c", "1"])
            prevButton = True
    else:
        button.led_bright = 0
        if prevButton:
            process.kill()
            prevButton = False
            speechInput = True

    if speechInput:
        speechInput = False
        text = Speech2Text()
        if text == "east":
            if current_tz == -12:
                current_tz = 11
            else:
                current_tz-=1
        elif text == "west":
            if current_tz == 11:
                current_tz = -12
            else:
                current_tz+=1  
        elif text == "day":
            DAYNIGHTFORCE = True
            DAYNIGHT = "day"
        elif text == "night":
            DAYNIGHTFORCE = True
            DAYNIGHT = "night"
        elif text == "shanghai":
            current_tz = -8
        elif text == "tokyo":
            current_tz = -9   
        elif text == "newyork":
            current_tz = 5          

    if not buttonA.value and not buttonB.value:
        current_tz = 5
    elif not buttonA.value and prevA:
        if current_tz == -12:
            current_tz = 11
        else:
            current_tz-=1
        prevA = buttonA.value
    elif not buttonB.value and prevB:
        if current_tz == 11:
            current_tz = -12
        else:
            current_tz+=1
        prevB = buttonB.value

    if prev_tz != current_tz:
        DAYNIGHTFORCE = False
        prev_tz = current_tz
    prevA = buttonA.value
    prevB = buttonB.value

    # Draw a black filled box to clear the image.
    NAME = time_zone_name[str(current_tz)] + "\n"
    TIME = datetime.now(pytz.timezone(time_zone_gmt[str(current_tz)])).strftime("%m/%d/%Y \n  %H:%M:%S") 
    HOUR = datetime.now(pytz.timezone(time_zone_gmt[str(current_tz)])).strftime("%H")
    HOUR = int(HOUR)

    if not DAYNIGHTFORCE:
        DAYNIGHT = "day"
        if HOUR >= 19 or HOUR <7:
        	DAYNIGHT = "night"

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    img_name = str(current_tz)+ DAYNIGHT+".jpg"
    background = Image.open(img_name)
    background = ScaleImage(background)
    draw = ImageDraw.Draw(background)

    if not buttonA.value:
        draw.rectangle((0,0,width,height),outline=0,fill = "#00FF00")
    elif not buttonB.value:
        draw.rectangle((0,0,width,height),outline=0,fill = "#FF0000")
 
    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 

    y=top
    EAST = "---------\n EAST |\n---------"
    WEST = "---------\n WEST |\n---------"
    draw.text((0,5),EAST, font=font, fill = "#00FF00")
    draw.text((0,75),WEST,font=font, fill = "#FF0000")
    draw.text((x+100, y+20), NAME, font=font, fill="#FFFFFF")
    draw.text((x+100, y+85), TIME, font=font, fill="#FFFFFF")

    # Display image.
    disp.image(background,rotation)
    #disp.image(image, rotation)
    #time.sleep(1)