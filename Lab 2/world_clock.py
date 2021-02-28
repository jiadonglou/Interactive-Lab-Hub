import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from datetime import datetime
import pytz 

time_zone_name = {
            "-12":"New Zealand Standard Time",
            "-11":"Solomon Standard Time",
            "-10":"Australia Eastern Time",
            "-9":"Japan Standard Time",
            "-8":"China Taiwan Time",
            "-7":"Vietnam Standard Time",
            "-6":"Bangladesh Standard Time",
            "-5":"Pakistan Lahore Time",
            "-4":"Near East Time",
            "-3":"Eastern African Time",
            "-2":"Egypt Standard Time",
            "-1":"European Central Time",
            "0":"Greenwich Mean Time",
            "1":"Central African Time",
            "2":"Fernando de Noronha Time",
            "3":"Argentina Standard Time",
            "4":"Puerto Rico Time",
            "5":"Eastern\nStandard Time",
            "6":"Central Standard Time",
            "7":"Phoenix Standard Time",
            "8":"Pacific Standard Time",
            "9":"Alaska Standard Time",
            "10":"Hawaii Standard Time",
            "11":"Midway Islands Time",
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
prevA = False
prevB = False

while True:
    if buttonA and not prevA:
        if current_tz == -12:
            current_tz = 11
        else:
            current_tz-=1
    else if buttonB and not prevB:
        if current_tz == 11:
            current_tz = -12
        current_tz+=1
    prevA = buttonA
    prevB = buttonB

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 
    NAME = time_zone_name[str(current_tz)] + "\n"
    TIME = datetime.now(pytz.timezone(time_zone_gmt[str(current_tz)])).strftime("%m/%d/%Y \n  %H:%M:%S") 
    y=top
    EAST = "---------\n EAST |\n---------"
    WEST = "---------\n WEST |\n---------"
    draw.text((0,5),EAST, font=font, fill = "#FFFFFF")
    draw.text((0,75),WEST,font=font, fill = "#FFFFFF")
    draw.text((x+75, y+20), NAME, font=font, fill="#FFFFFF")
    draw.text((x+100, y+85), TIME, font=font, fill="#FFFFFF")

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)