import paho.mqtt.client as mqtt
import uuid
import pandas as pd

# the # wildcard means we subscribe to all subtopics of IDD


# some other examples
# topic = 'IDD/a/fun/topic'

def parse_data(side,msg):
	msg_split = msg.payload.decode('UTF-8').split('+')
	if msg_split[0] in df['timestamp']:
		idx = df[df['timestamp']== msg_split[0]].index.values
		df[side][idx] = msg_split[1]
	else:
		tempdf = {'timestamp': msg_split[0], side: msg_split[1]}
		df = df.append(tempdf, ignore_index = True)
    df.to_csv (r'result.csv', index = False, header=True)

#this is the callback that gets called once we connect to the broker. 
#we should add our subscribe functions here as well
def on_connect(client, userdata, flags, rc):
	print(f"connected with result code {rc}")
	client.subscribe(topic)
	# you can subsribe to as many topics as you'd like
	# client.subscribe('some/other/topic')


# this is the callback that gets called each time a message is recived
def on_message(cleint, userdata, msg):
	print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}")
	# you can filter by topics
	if msg.topic == 'IDD/left':
		parse_data('left',msg)
	elif msg.topic == 'IDD/left':
		parse_data('right',msg)



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

df = pd.read_csv (r'./output.csv')
# this is blocking. to see other ways of dealing with the loop
#  https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php#network-loop
client.loop_forever()