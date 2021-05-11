import paho.mqtt.client as mqtt
import uuid
from datetime import datetime

import time
from math import atan2, degrees
import board
import adafruit_mpu6050
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


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


i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_mpu6050.MPU6050(i2c)

def draw_red():
	disp.image(image, rotation)
	draw.rectangle((0, 0, width, height), outline=0, fill=(255,0,0))

def draw_green():
	disp.image(image, rotation)
	draw.rectangle((0, 0, width, height), outline=0, fill=(0,255,0))

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe('IDD/ski/right')
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
	#print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
	# you can filter by topics
	if msg.topic == 'IDD/ski/carving':
		if int(msg.payload.decode('UTF-8')):
			draw_green()
		else:
			draw_red()


# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')



# attach out callbacks to the client
client.on_connect = on_connect
client.on_message = on_message

#connect to the broker
client.connect(
	'farlab.infosci.cornell.edu',
	port=8883)
topic = f"IDD/ski/left"

# Given a point (x, y) return the angle of that point relative to x axis.
# Returns: angle in degrees

def myround(x, base=5):
    return base * round(x/base)

def vector_2_degrees(x, y):
	angle = degrees(atan2(y, x))
	if angle < 0:
		angle += 360
	angle = int(angle)
	angle = myround(angle)
	return 180-angle


# Given an accelerometer sensor object return the inclination angles of X/Z and Y/Z
# Returns: tuple containing the two angles in degrees


def get_inclination(_sensor):
	x, y, z = _sensor.acceleration
	return vector_2_degrees(x, z), vector_2_degrees(y, z)

client.loop_start()
while True:
	angle_xz, angle_yz = get_inclination(sensor)
	#output = "{:6.2f}-{:6.2f}".format(angle_xz, angle_yz)
	output = "{:6.2f}".format(angle_xz)
	#timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	#timestamp=timestamp[:21]
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	val = timestamp + "+"+ output
	client.publish(topic, val)
	time.sleep(0.1)

