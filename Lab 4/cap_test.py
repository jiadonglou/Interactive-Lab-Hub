import time
import board
import busio

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)
#mpr121.threshold(0,10)
th = 10;
test = False

while True:
	if mpr121[1].value:
		test = True
	else:
		test = False

	if test:
		mpr121[1].threshold=th
		th+=1
		print(mpr121[1].threshold)

	for i in range(12):
		if mpr121[i].value:
			#print(f"Banana {i} touched!")
	#time.sleep(0.25)  # Small delay to keep from spamming output messages.