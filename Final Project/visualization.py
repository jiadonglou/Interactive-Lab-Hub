import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



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
	plt.ylim([0, 30])
	plt.legend(loc='upper left')
	plt.xlabel('Orange: Left board angle. Blue: Right board angle')
	plt.ylabel('Time')

ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.show()
