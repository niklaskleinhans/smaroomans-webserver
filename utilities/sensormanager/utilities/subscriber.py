'''
subscriber for sensors
'''

from threads.stopableThread import StopableThread
from models.notification import Notification
import json
import time


class Subscriber():
    def __init__(self, database, host, publisher, mqtt):
        self.host = host
        self.mqtt = mqtt
        self.DB = database
        self.publisher = publisher

    def on_message(self, client, userdata, message):
        '''
        check if messages are relevant and map

        Parameters
        ----------
        client: mqtt client
        userdata:mqtt userdata
        message: mqtt message
        '''
        if message.topic == 'zwave/updates/2':
            self.on_message_from_multisensor(client, userdata, message)
        if message.topic == 'plugwise2py/state/energy/000D6F0004B1E6C4':
            self.on_message_from_plugwise1(client, userdata, message)
        if message.topic == 'plugwise2py/state/circle/000D6F0004B1E6C4':
            self.on_message_from_plugwise1(client, userdata, message)
        if message.topic == 'plugwise2py/state/energy/000D6F0005692B55':
            self.on_message_from_plugwise2(client, userdata, message)
        if message.topic == 'plugwise2py/state/circle/000D6F0005692B55':
            self.on_message_from_plugwise2(client, userdata, message)
        if message.topic == 'gpio/sensor/window':
            self.on_message_from_gpio(client, userdata, message)

    def on_message_from_multisensor(self, client, userdata, message):
        '''
        store and publish multisensor messages

        Parameters
        ----------
        client: mqtt client
        userdata:mqtt userdata
        message: mqtt message
        '''
        message = json.loads(message.payload.decode())
        key = [key for key in message][0]
        self.DB.updateSensorData('multisensor_' + str(key), message)
        topic = self.DB.getSensorTopic('multisensor_' + str(key))
        publisherMessage = {'data': message, 'room': '', 'sensortype':'', 'key':''}
        try:
            sensor = self.DB.getSensor('multisensor_' + str(key)) 
            sensorkey = sensor['key'] if sensor['key'] is not None else ''
            room = sensor['room'] if sensor['room'] is not None else ''
            sensortype = sensor['sensortype'] if sensor['sensortype'] is not None else ''
            publisherMessage['key'] = sensorkey
            publisherMessage['room'] = room
            publisherMessage['sensortype'] = sensortype
        except Exception as e:
            print('multisensor', e, message)
            pass
        if topic is not None:
            self.publisher.publish(topic, publisherMessage)

    def on_message_from_plugwise1(self, client, userdata, message):
        '''
        store and publish plugwise one messages

        Parameters
        ----------
        client: mqtt client
        userdata:mqtt userdata
        message: mqtt message
        '''
        message = json.loads(message.payload.decode())
        keys = [key for key in message]
        for key in keys:
            self.DB.updateSensorData(
                'plugwise1_' + str(key), {str(key): message[key]})
            topic = self.DB.getSensorTopic('plugwise1_' + str(key))
            publisherMessage = {'data': {key: message[key]}, 'room': ''}
            try:
                sensor = self.DB.getSensor('plugwise1_' + str(key))
                sensorkey = sensor['key'] if sensor['key'] is not None else ''
                room = sensor['room'] if sensor['room'] is not None else ''
                sensortype = sensor['sensortype'] if sensor['sensortype'] is not None else ''
                publisherMessage['key'] = sensorkey
                publisherMessage['room'] = room
                publisherMessage['sensortype'] = sensortype
            except Exception as e:
                print('plugwise1', e)
                pass
            if topic is not None:
                self.publisher.publish(topic, publisherMessage)

    def on_message_from_plugwise2(self, client, userdata, message):
        '''
        store and publish plugwise two messages

        Parameters
        ----------
        client: mqtt client
        userdata:mqtt userdata
        message: mqtt message
        '''
        message = json.loads(message.payload.decode())
        keys = [key for key in message]
        for key in keys:
            self.DB.updateSensorData(
                'plugwise2_' + str(key), {str(key): message[key]})
            topic = self.DB.getSensorTopic('plugwise2_' + str(key))
            publisherMessage = {'data': {key: message[key]}, 'room': ''}
            try:
                sensor = self.DB.getSensor('plugwise2_' + str(key))
                sensorkey = sensor['key'] if sensor['key'] is not None else ''
                room = sensor['room'] if sensor['room'] is not None else ''
                sensortype = sensor['sensortype'] if sensor['sensortype'] is not None else ''
                publisherMessage['key'] = sensorkey
                publisherMessage['room'] = room
                publisherMessage['sensortype'] = sensortype
            except Exception as e:
                print('plugwise2', e)
                pass
            if topic is not None:
                self.publisher.publish(topic, publisherMessage)

    def on_message_from_gpio(self, client, userdata, message):
        '''
        store and publish gpio messages

        Parameters
        ----------
        client: mqtt client
        userdata:mqtt userdata
        message: mqtt message
        '''
        message = json.loads(message.payload.decode())
        key = [key for key in message][0]
        self.DB.updateSensorData('gpiosensor_' + str(key), message)
        topic = self.DB.getSensorTopic('gpiosensor_' + str(key))
        publisherMessage = {'data': message, 'room': ''}
        try:
            sensor = self.DB.getSensor('gpiosensor_' + str(key))
            sensorkey = sensor['key'] if sensor['key'] is not None else ''
            room = sensor['room'] if sensor['room'] is not None else ''
            sensortype = sensor['sensortype'] if sensor['sensortype'] is not None else ''
            publisherMessage['key'] = sensorkey
            publisherMessage['room'] = room
            publisherMessage['sensortype'] = sensortype
        except Exception as e:
            print('gpio', e)
            pass
        if topic is not None:
            self.publisher.publish(topic, publisherMessage)

    def startSubscription(self):
        '''
        init all subscriber for sensors
        '''
        self.mqtt.subscribe('zwave/updates/2')
        self.mqtt.subscribe("plugwise2py/state/energy/000D6F0004B1E6C4")
        self.mqtt.subscribe("plugwise2py/state/circle/000D6F0004B1E6C4")
        self.mqtt.subscribe("plugwise2py/state/energy/000D6F0005692B55")
        self.mqtt.subscribe("plugwise2py/state/circle/000D6F0005692B55")
        self.mqtt.subscribe("gpio/sensor/window")
