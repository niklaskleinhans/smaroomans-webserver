'''
Database Service
'''


from flask_pymongo import PyMongo
from models.room import Room
from models.user import User
from models.sensor import Sensor
from models.actuator import Actuator
from models.roommap import Roommap
import utilities.util as util
import threading
import time
import numpy as np
import datetime


class DB():
    def __init__(self, app):
        app.config['MONGO_URI'] = "mongodb://localhost:27017/smaroomansDatabase"
        self.mongo = PyMongo(app)
        print('init DB')
        self.sensorlock = threading.Lock()
        self.roomlock = threading.Lock()
        self.userlock = threading.Lock()

    def getAllRooms(self):
        """
        returns all Rooms

        Returns
        -------
        list
            list with all Rooms as model dict
        """
        rooms = []
        for room in self.mongo.db.room.find():
            try:
                room['active'] = self.getRoomState(
                    room['key'], datetime.datetime.now().strftime('%Y-%m-%d'))
                room['users'] = self.getRoomUsers(
                    room['key'], datetime.datetime.now().strftime('%Y-%m-%d'))
                rooms.append(Room(**room).getDict())
            except Exception as e:
                print(e)
        return rooms

    def getAllSensors(self):
        """
        returns all Sensors

        Returns
        -------
        moongodb.cursor
            iterator with all sensors
        """
        return self.mongo.db.sensor.find()

    def getAllActuators(self):
        """
        returns all Actuators

        Returns
        -------
        moongodb.cursor
            iterator with all actuators
        """
        return self.mongo.db.actuator.find()

    def getAllUsers(self):
        """
        returns all Users

        Returns
        -------
        moongodb.cursor
            iterator with all Users
        """
        return self.mongo.db.user.find()

    def setUserPlan(self, user, workplan):
        """
        update user workplan

        Parameters
        -------
        user: str
            user key as string
        workplan: list
            user workplan as list
        """
        self.mongo.db.user.update_one(
            {'key': user}, {'$set': {'workplan': workplan}}, upsert=True)

    def appendNotification(self, room, notification):
        """
        append Notifications to room

        Parameters
        -------
        room: str
            room key as string
        notification: list
            notifications for room as list
        """
        roomNotifications = self.mongo.db.room.find_one({'key': room})[
            'notifications']
        roomNotifications.append(notification)
        try:
            self.mongo.db.room.update_one(
                {'key': room}, {'$set': {'notifications': roomNotifications}}, upsert=False)
        except Exception as e:
            print(e)

    def clearAllNotifications(self):
        """
        deletes all room Notifications
        """
        try:
            for room in self.getAllRooms():
                self.mongo.db.room.update_one(
                    {'key': room['key']}, {'$set': {'notifications': []}}, upsert=False)
        except Exception as e:
            print(e)

    def updateSensorData(self, key, data):
        """
        update sensor data information

        Parameters
        -------
        key: str
            sensor key as string
        data: dict
            sensor data as key value pair
        """
        key = str(key).replace(" ", "_")
        self.mongo.db.sensor.update_one(
            {'key': key}, {'$set': {'data': data}}, upsert=True)

    def getSensorTopic(self, key):
        """
        returns Sensor topic information

        Parameters
        -------
        key: str
            sensor key as string

        Returns
        -------
        string
            topic as string
        """
        key = str(key).replace(" ", "_")
        sensor = self.mongo.db.sensor.find_one({'key': key})
        if sensor is not None:
            topic = 'sensor'+'/'+str(key)
            return topic
        else:
            return None

    def getSensorData(self, key):
        """
        returns Sensor data information

        Parameters
        -------
        key: str
            sensor key as string

        Returns
        -------
        dict
            key value pair with sensor data
        """
        key = str(key).replace(" ", "_")
        sensor = self.mongo.db.sensor.find_one({'key': key})
        #if key in self.sensorCache : sensor['data'] = self.sensorCache[key]
        return sensor['data'] if sensor is not None else None

    def getSensor(self, key):
        """
        returns Sensor model as dict

        Parameters
        -------
        key: str
            sensor key as string

        Returns
        -------
        dict
            complete sensor information as dict
        """
        key = str(key).replace(" ", "_")
        sensor = self.mongo.db.sensor.find_one({'key': key})
        #if key in self.sensorCache : sensor['data'] = self.sensorCache[key]
        return sensor if sensor is not None else None

    def getRoomSensors(self, room):
        # TODO maybe just return key?
        """
        returns Sensor models as dict of room 

        Parameters
        -------
        room: str
            room key as string

        Returns
        -------
        list
            dicts with sensor informations
        """
        sensordata = []
        sensors = self.mongo.db.room.find_one({'key': room})['sensors']
        for sensor in sensors:
            sensordata.append({'key': sensor,
                               'sensortopic': self.getSensorTopic(sensor),
                               'data': self.getSensorData(sensor)})
        return sensordata

    def getRoomActuatorTopicAndData(self, room, actuatorType):
        """
        returns actuator topic and topicdata

        Parameters
        -------
        room: str
            room key as string
        actuatortype: str
            actuator type

        Returns
        -------
        string
            actuatortopic
        string
            actuatordata
        """
        roomActuators = self.mongo.db.room.find_one({'key': room})['actuators']
        actuators = []
        for actuator in roomActuators:
            actuators.append(
                self.mongo.db.actuator.find_one({'key': actuator}))
        actuatorTopic = None
        actuatorData = None
        for actuator in actuators:
            if actuator['actuatortype'] == actuatorType:
                actuatorTopic = actuator['topic']
                actuatorData = actuator['topicdata']
        return actuatorTopic, actuatorData

    def getRoomTemperature(self, room):
        """
        returns room temperature

        Parameters
        -------
        room: str
            room key as string

        Returns
        -------
        int
            temperature
        """
        roomSensors = self.mongo.db.room.find_one({'key': room})['sensors']
        for roomSensor in roomSensors:
            sensor = self.mongo.db.sensor.find_one({'key': roomSensor})
            if sensor['sensortype'] == 'temperature':
                return sensor['data']['Temperature']

    def getRoomWindowStatus(self, room):
        """
        returns window status of room

        Parameters
        -------
        room: str
            room key as string

        Returns
        -------
        int
            0: closed
            1: open
        """
        roomSensors = self.mongo.db.room.find_one({'key': room})['sensors']
        for roomSensor in roomSensors:
            sensor = self.mongo.db.sensor.find_one({'key': roomSensor})
            if sensor['sensortype'] == 'window':
                return sensor['data']['window']

    def getRoomLuminance(self, room):
        """
        returns luminance of room

        Parameters
        -------
        room: str
            room key as string

        Returns
        -------
        int
            luminance
        """
        roomSensors = self.mongo.db.room.find_one({'key': room})['sensors']
        for roomSensor in roomSensors:
            sensor = self.mongo.db.sensor.find_one({'key': roomSensor})
            if sensor['sensortype'] == 'luminance':
                return sensor['data']['Luminance']

    def getRoomLightState(self, room):
        """
        returns light state of room

        Parameters
        -------
        room: str
            room key as string

        Returns
        -------
        string
            'on'/'off'
        """
        roomSensors = self.mongo.db.room.find_one({'key': room})['sensors']
        for roomSensor in roomSensors:
            sensor = self.mongo.db.sensor.find_one({'key': roomSensor})
            if sensor['sensortype'] == 'lightswitch':
                return sensor['data']['switch']

    def getRoomFanState(self, room):
        """
        returns fan state of room

        Parameters
        -------
        room: str
            room key as string

        Returns
        -------
        string
            'on'/'off
        """
        roomSensors = self.mongo.db.room.find_one({'key': room})['sensors']
        for roomSensor in roomSensors:
            sensor = self.mongo.db.sensor.find_one({'key': roomSensor})
            if sensor['sensortype'] == 'fanswitch':
                return sensor['data']['switch']

    def getRoomState(self, room, date):
        """
        returns current room state of room

        Parameters
        -------
        room: str
            room key as string

        Returns
        -------
        bool
            True: room is active
            False: room is in stanbymode
        """
        try:
            roommap = self.mongo.db.roommanager.find_one(
                {'datum': util.datumToSeconds(date), 'room': room})
            if roommap is not None:
                return roommap['active']
            else:
                return True
        except Exception as e:
            print(e)
        return False

    def getRoomUsers(self, room, date):
        """
        returns all mapped user for the room at specific date

        Parameters
        -------
        room: str
            room key as string
        date: str
            date string in format %Y-%m-%d

        Returns
        -------
        list
            userkeys
        """
        try:
            roommap = self.mongo.db.roommanager.find_one(
                {'datum': util.datumToSeconds(date), 'room': room})
            if roommap is not None:
                return roommap['users']
            else:
                return []
        except Exception as e:
            print(e)
        return []

    def getRoomMapsByDatum(self, timebegin, timeend):
        """
        returns all roommaps in timerange

        Parameters
        -------
        timebegin: str
            date string for first date in format %Y-%m-%d
        timeend: str
            date string for last date in format %Y-%m-%d

        Returns
        -------
        mongodb.cursors
            iterator with all roommaps
        """
        datumbegin = util.datumToSeconds(timebegin)
        datumend = util.datumToSeconds(timeend)
        roommaps = self.mongo.db.roommanager.find(
            {'datum': {"$gte": datumbegin, "$lte": datumend}})
        return roommaps

    def updateRoomMap(self, roommap):
        """
        update roommap entry in roommanager db

        Parameters
        -------
        roommap:dict
            roommap model as dict

        """
        self.mongo.db.roommanager.update_one({'datum': util.datumToSeconds(roommap['datum']), 'room': roommap['room']},
                                             {'$set': {'users': roommap['users'], 'active': roommap['active']}}, upsert=True)

    ###### Initialization #####
    def _setSensorRooms(self):
        '''
        set room information in sensor entry 
        '''
        for sensor in self.getAllSensors():
            print('sensor:', sensor)
            for room in self.getAllRooms():
                if sensor['key'] in room['sensors']:
                    print('update:', sensor['key'], room['key'])
                    self.mongo.db.sensor.update_one({'key': sensor['key']}, {
                                                    '$set': {'room': room['key']}}, upsert=True)

    def _setActuatorRooms(self):
        '''
        set room information in actuator entry
        '''
        for actuator in self.getAllActuators():
            for room in self.getAllRooms():
                if actuator['key'] in room['actuators']:
                    self.mongo.db.actuator.update_one({'key': actuator['key']}, {
                                                      '$set': {'room': room['key']}}, upsert=True)

    def _initialisation(self):
        '''
        Database initialisation
        '''
        # delete all tables
        self.mongo.db.sensor.drop()
        self.mongo.db.user.drop()
        self.mongo.db.room.drop()
        self.mongo.db.actuator.drop()
        self.mongo.db.roommanager.drop()

        # insert sensors
        self.mongo.db.sensor.insert(Sensor(
            key='multisensor_Relative_Humidity', sensortype='humidity', data={'Humidity': 0}).getDict())
        self.mongo.db.sensor.insert(Sensor(
            key='multisensor_Temperature', sensortype='temperature', data={'Temperature': 0}).getDict())
        self.mongo.db.sensor.insert(
            Sensor(key='multisensor_Ultraviolet').getDict())
        self.mongo.db.sensor.insert(
            Sensor(key='multisensor_Group_1_Interval').getDict())
        self.mongo.db.sensor.insert(Sensor(
            key='multisensor_Luminance', sensortype='luminance', data={'Luminance': 30}).getDict())

        self.mongo.db.sensor.insert(Sensor(key='plugwise1_type').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_typ').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_ts').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_mac').getDict())
        self.mongo.db.sensor.insert(
            Sensor(key='plugwise1_power', sensortype='lightpower').getDict())
        self.mongo.db.sensor.insert(
            Sensor(key='plugwise1_switch', sensortype='lightswitch').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_energy').getDict())
        self.mongo.db.sensor.insert(
            Sensor(key='plugwise1_cum_energy').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_pwenergy').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_power82').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_powerts').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_name').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_schedule').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_requid').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_power1s').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_switcheq').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_readonly').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise1_interval').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_type').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_typ').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_ts').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_mac').getDict())
        self.mongo.db.sensor.insert(
            Sensor(key='plugwise2_power', sensortype='fanpower').getDict())
        self.mongo.db.sensor.insert(
            Sensor(key='plugwise2_switch', sensortype='fanswitch').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_energy').getDict())
        self.mongo.db.sensor.insert(
            Sensor(key='plugwise2_cum_energy').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_pwenergy').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_power82').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_powerts').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_name').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_schedule').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_requid').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_power1s').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_switcheq').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_readonly').getDict())
        self.mongo.db.sensor.insert(Sensor(key='plugwise2_interval').getDict())
        self.mongo.db.sensor.insert(Sensor(
            key='gpiosensor_window', sensortype='window', data={'window': 0}).getDict())
        for i in range(19):
            self.mongo.db.sensor.insert(
                Sensor(key='sensor' + str(i)).getDict())

        # insers actuators
        self.mongo.db.actuator.insert(Actuator(
            key='stateled1', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled2', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled3', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled4', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled5', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled6', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled7', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled8', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled9', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='stateled10', actuatortype='stateled', topicdata={'data': 0}).getDict())
        self.mongo.db.actuator.insert(Actuator(
            key='notificationrgbled1', actuatortype='notificationrgbled', topicdata={'state': [0, 0, 0]}).getDict())
        self.mongo.db.actuator.insert(Actuator(key='light1', actuatortype='light',
                                               topic='plugwise2py/cmd/switch/000D6F0004B1E6C4', topicdata={'mac': "", "cmd": "switch", "val": "off"}).getDict())
        self.mongo.db.actuator.insert(Actuator(key='fan1', actuatortype='fan', topic='plugwise2py/cmd/switch/000D6F0005692B55',
                                               topicdata={'mac': "", "cmd": "switch", "val": "off"}).getDict())

        # insert Rooms
        self.mongo.db.room.insert(Room(key='room1', maxStaff=5, sensors=['multisensor_Relative_Humidity',
                                                                         'multisensor_Temperature',
                                                                         'multisensor_Ultraviolet',
                                                                         'multisensor_Luminance',
                                                                         'multisensor_Group_1_Interval',
                                                                         'gpiosensor_window',
                                                                         'plugwise1_power',
                                                                         'plugwise1_switch',
                                                                         'plugwise1_energy',
                                                                         'plugwise1_cum_energy',
                                                                         'plugwise1_interval',
                                                                         'plugwise2_power',
                                                                         'plugwise2_switch',
                                                                         'plugwise2_energy',
                                                                         'plugwise2_cum_energy',
                                                                         'plugwise2_interval'], actuators=['stateled1', 'notificationrgbled1', 'light1', 'fan1'], users=['staff1', 'staff2']).getDict())
        self.mongo.db.room.insert(Room(key='room2', maxStaff=3, sensors=[
                                  'sensor1', 'sensor2'], actuators=['stateled2']).getDict())
        self.mongo.db.room.insert(Room(key='room3', maxStaff=3, sensors=[
                                  'sensor3', 'sensor4'], actuators=['stateled3']).getDict())
        self.mongo.db.room.insert(Room(key='room4', maxStaff=3, sensors=[
                                  'sensor5', 'sensor6'], actuators=['stateled4']).getDict())
        self.mongo.db.room.insert(Room(key='room5', maxStaff=3, sensors=[
                                  'sensor7', 'sensor8'], actuators=['stateled5']).getDict())
        self.mongo.db.room.insert(Room(key='room6', maxStaff=3, sensors=[
                                  'sensor9', 'sensor10'], actuators=['stateled6']).getDict())
        self.mongo.db.room.insert(Room(key='room7', maxStaff=3, sensors=[
                                  'sensor11', 'sensor12'], actuators=['stateled7']).getDict())
        self.mongo.db.room.insert(Room(key='room8', maxStaff=3, sensors=[
                                  'sensor13', 'sensor14'], actuators=['stateled8']).getDict())
        self.mongo.db.room.insert(Room(key='room9', maxStaff=3, sensors=[
                                  'sensor15', 'sensor16'], actuators=['stateled9']).getDict())
        self.mongo.db.room.insert(Room(key='room10', maxStaff=3, sensors=[
                                  'sensor17', 'sensor18'], actuators=['stateled10']).getDict())

        # insert User
        for i in range(41):
            self.mongo.db.user.insert(User(key='staff' + str(i)).getDict())

        # insert roommaps
        self.mongo.db.roommanager.insert(Roommap(util.datumToSeconds(
            "2019-07-15"), 'room1', users=['staff1', 'staff2']).getDict())
        self.mongo.db.roommanager.insert(Roommap(util.datumToSeconds(
            "2019-07-15"), 'room3', users=['staff10', 'staff12']).getDict())
        self.mongo.db.roommanager.insert(Roommap(util.datumToSeconds(
            "2019-07-15"), 'room7', users=['staff20', 'staff21']).getDict())
        self.mongo.db.roommanager.insert(
            Roommap(util.datumToSeconds("2019-07-16"), 'room1', users=[]).getDict())

        # add relations into database
        self._setSensorRooms()
        self._setActuatorRooms()
