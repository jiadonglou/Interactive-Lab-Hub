import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import paho.mqtt.client as mqtt
import uuid
from datetime import datetime


x=[]
y=[]


def animate(i):
	csv_file='result.csv'
	data = pd.read_csv(csv_file)

	Time = data["timestamp"]
	Left = data["left"]
	Right = data["right"]

	x=list(Right)
	x = [each+180 for each in x]

	y=list(Left)

	if len(x)>30:
		x = x[-30:]		
	if len(y)>30:
		y = y[-30:]


	temp = list(range(0,len(x)))


	plt.cla()

	plt.plot(x,temp, label='Right board')
	plt.plot(y,temp, label='Left board')
	plt.xlim([0, 360])
	plt.ylim([0, 40])
	plt.legend(loc='upper left')
	plt.xlabel('Orange: Left board angle. Blue: Right board angle')
	plt.ylabel('Time')

	if abs(x[-1]-180 - y[-1])<11:
		text_kwargs = dict(ha='center', va='center', fontsize=28, color='g')
		plt.text(180, 35, 'Carving', **text_kwargs)
		client.publish(topic, 1)
	else:
		text_kwargs = dict(ha='center', va='center', fontsize=28, color='r')
		plt.text(180, 35, 'Not Carving', **text_kwargs)
		client.publish(topic, 0)

	

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
topic = f"IDD/ski/carving"
ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()
