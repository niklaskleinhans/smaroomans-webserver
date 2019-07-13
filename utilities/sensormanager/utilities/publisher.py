import json
import time
import datetime


class Publisher():
    def __init__(self, database, host, mqtt):
        self.host = host
        self.mqtt = mqtt
        self.DB = database

    def publishRoomNotifications(self):
        for room in self.DB.getAllRooms():
            for user in self.DB.getRoomUsers(room['key'], datetime.datetime.now().strftime('%Y-%m-%d')):
                notification = {'data': room['notifications'], 'user': user}
                self.mqtt.publish('client/notifications',
                                  json.dumps(notification))
                if len(room['notifications']) > 0 and room['key'] == 'room1':
                    self.mqtt.publish(
                        'actuator/notificationrgbled', json.dumps({'room': 'room1', 'state': [0, 0, 1]}))
                if len(room['notifications']) == 0 and room['key'] == 'room1':
                    self.mqtt.publish(
                        'actuator/notificationrgbled', json.dumps({'room': 'room1', 'state': [0, 0, 0]}))
                #print('published: ', str(notification))

    def on_connect(self, client, userdata, flags, rc):
        print("publisher client connected", rc)

    def on_disconnect(self, client, userdata, rc):
        print("publisher client disconnected", rc)

    def publish(self, topic, data):
        #print(topic, data)
        self.mqtt.publish(topic=topic, payload=json.dumps(data), retain=True)
