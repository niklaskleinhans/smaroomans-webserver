'''
sensormanager to organize subscriber and publisher
'''

from utilities.sensormanager.utilities.subscriber import Subscriber
from utilities.sensormanager.utilities.publisher import Publisher


class SensorManager():
    def __init__(self, database, host, mqtt):
        self.DB = database
        self.mqtt = mqtt
        # init publisher and subscriber
        self.publisher = Publisher(self.DB, host, mqtt)
        self.subscriber = Subscriber(self.DB, host, self.publisher, self.mqtt)
        #set initial sensor intervals
        self.publisher.publish('zwave/set/2', {'Group 1 Interval': 5})
        self.publisher.publish('zwave/set/2', {"Wake-up Interval": 240})
        self.publisher.publish('zwave/set/2',  {"On time": 10})

    def on_connect(self, client, userdata, flags, rc):
        print("publisher client connected", rc)

    def on_disconnect(self, client, userdata, rc):
        print("publisher client disconnected", rc)
