import paho.mqtt.client as mqtt
import uuid
from datetime import datetime

import time
from math import atan2, degrees
import board
import adafruit_mpu6050

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_mpu6050.MPU6050(i2c)

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

#connect to the broker
client.connect(
	'farlab.infosci.cornell.edu',
	port=8883)
topic = f"IDD/ski/right"

# Given a point (x, y) return the angle of that point relative to x axis.
# Returns: angle in degrees


def vector_2_degrees(x, y):
	angle = degrees(atan2(y, x))
	if angle < 0:
		angle += 360
	return angle


# Given an accelerometer sensor object return the inclination angles of X/Z and Y/Z
# Returns: tuple containing the two angles in degrees


def get_inclination(_sensor):
	x, y, z = _sensor.acceleration
	return vector_2_degrees(x, z), vector_2_degrees(y, z)

while True:
	angle_xz, angle_yz = get_inclination(sensor)
	#output = "{:6.2f}-{:6.2f}".format(angle_xz, angle_yz)
	output = "{:6.2f}".format(angle_xz)
	timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	val = timestamp + "+"+ output
	client.publish(topic, val)
	time.sleep(0.1)

