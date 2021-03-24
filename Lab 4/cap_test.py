import time
import board
import busio

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)
#mpr121.threshold(0,10)

while True:
	mpr121[1].threshold=85

	for i in range(12):
		if mpr121[i].value:
			print(f"Banana {i} touched!")
	time.sleep(0.25)  # Small delay to keep from spamming output messages.