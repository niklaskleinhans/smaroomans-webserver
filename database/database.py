from tinydb import TinyDB, Query, where
from models.room import Room
from models.user import User
from models.sensor import Sensor
from models.actuator import Actuator
import numpy as np

roomDB = TinyDB('database/content/room.json')
usersDB = TinyDB('database/content/users.json')
sensorsDB = TinyDB('database/content/sensors.json')
organizerDB = TinyDB('database/content/organizer.json')
actuatorsDB = TinyDB('database/content/actuators.json')

class DB():
    def __init__(self):
        print('init DB')
    
    def getAllRooms(self):
        return roomDB.all()
    
    def getAllSensors(self):
        return sensorsDB.all()
    
    def getAllActuators(self):
        return actuatorsDB.all()

    def updateSensorData(self, key, data):
        key = str(key).replace(" ","_")
        sensorQuery = Query()
        sensor = sensorsDB.get(where('key')==key)
        if sensor is not None:
            sensorsDB.upsert({'key': key, 'data': data }, sensorQuery.key == key)
        else:
            sensorsDB.insert(Sensor(key=key,data=data).getDict())

    def updateSensorRoom(self, key, room):
        key = str(key).replace(" ", "_")
        sensorQuery = Query()
        sensorsDB.update({'room': room }, sensorQuery.key == key )

    def getSensorTopic(self, key):
        key = str(key).replace(" ", "_")
        sensor = sensorsDB.get(where('key')==key)
        if sensor is not None:
            topic='sensor'+'/'+str(key)
            return topic
        else:
            return None
    
    def getActuatorTopic(self, key):
        key = str(key).replace(" ", "_")
        actuator = actuatorsDB.get(where('key')==key)
        if actuator is not None:
            topic='actuator'
            topic = topic+"/"+str(actuator['actuatortype'])
            return topic
        else:
            return None

    def getSensorData(self, key):
        key = str(key).replace(" ", "_")
        sensor = sensorsDB.get(where('key')==key)
        return sensor if sensor is not None else None 


    def getRoomData(self, room):
        roomQuery = Query()
        sensorQuery = Query()
        sensorData = []
        sensors = roomDB.get(where('room')==room)['sensors']
        for sensor in sensors:
            sensorData.append(sensorsDB.get(where('key') == sensor)['data'])
    
    def getRoomSensors(self, room):
        sensordata=[]
        sensors = roomDB.get(where('key')==room)['sensors']
        for idx , sensor in enumerate(sensors):
            sensordata.append({'key': sensor,
                               'sensortopic': self.getSensorTopic(sensor),
                               'data': self.getSensorData(sensor)})
        return sensordata

    def _setSensorRooms(self):
        sensors = self.getAllSensors()
        sensorQuery=Query()
        rooms = self.getAllRooms()
        for sensor in sensors:
            for room in rooms:
                if sensor['key'] in room['sensors']:
                    sensorsDB.update({'key': sensor['key'], 'room': room['key'] }, sensorQuery.key == sensor['key'])
    
    def _setActuatorRooms(self):
        actuators = self.getAllActuators()
        rooms = self.getAllRooms()
        for actuator in actuators:
            for room in rooms:
                if actuator['key'] in room['actuators']:
                    actuatorsDB.update({'key': actuator['key'], 'room': room['key'] }, where('key') == actuator['key'])

    def _initialisation(self):
        roomDB.purge()
        usersDB.purge()
        actuatorsDB.purge_tables()
        sensorsDB.insert(Sensor(key='multisensor_Relative_Humidity').getDict())
        sensorsDB.insert(Sensor(key='multisensor_Temperature').getDict())
        sensorsDB.insert(Sensor(key='multisensor_Ultraviolet').getDict())
        sensorsDB.insert(Sensor(key='multisensor_Group_1_Interval').getDict())
        sensorsDB.insert(Sensor(key='plugwise1_type').getDict())
        sensorsDB.insert(Sensor(key='plugwise1_ts').getDict())
        sensorsDB.insert(Sensor(key='plugwise1_mac').getDict())
        sensorsDB.insert(Sensor(key='plugwise1_power').getDict())
        sensorsDB.insert(Sensor(key='plugwise1_energy').getDict())
        sensorsDB.insert(Sensor(key='plugwise1_cum_energy').getDict())
        sensorsDB.insert(Sensor(key='plugwise1_interval').getDict())
        sensorsDB.insert(Sensor(key='gpiosensor_window').getDict())
        actuatorsDB.insert(Actuator(key='stateled1', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled2', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled3', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled4', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled5', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled6', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled7', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled8', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled9', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='stateled10', actuatortype='stateled', data={'data': 0}).getDict())
        actuatorsDB.insert(Actuator(key='notificationrgbled1', actuatortype='notificationrgbled', data={'state': [0,0,0]}).getDict())
        actuatorsDB.insert(Actuator(key='light1', actuatortype='plugwise2py/cmd/switch/000D6F0004B1E6C4', data={'mac':"", "cmd":"switch", "val":"off"}).getDict())

        for i in range(19):
            sensorsDB.insert(Sensor(key='sensor'+ str(i)).getDict())
        roomDB.insert(Room(key='room1',maxStaff=5,sensors=['multisensor_Relative_Humidity', 
                                                           'multisensor_Temperature',
                                                           'multisensor_Ultraviolet', 
                                                           'multisensor_Luminance', 
                                                           'multisensor_Group_1_Interval',
                                                           'gpiosensor_window',
                                                           'plugwise1_power', 
                                                           'plugwise1_energy', 
                                                           'plugwise1_cum_energy',
                                                           'plugwise1_interval'], actuators=['stateled1', 'notificationrgbled1', 'light1']).getDict())
        roomDB.insert(Room(key='room2',maxStaff=3,sensors=['sensor1', 'sensor2'], actuators=['stateled2']).getDict())
        roomDB.insert(Room(key='room3',maxStaff=3,sensors=['sensor3', 'sensor4'], actuators=['stateled3']).getDict())
        roomDB.insert(Room(key='room4',maxStaff=3,sensors=['sensor5', 'sensor6'], actuators=['stateled4']).getDict())
        roomDB.insert(Room(key='room5',maxStaff=3,sensors=['sensor7', 'sensor8'], actuators=['stateled5']).getDict())
        roomDB.insert(Room(key='room6',maxStaff=3,sensors=['sensor9', 'sensor10'], actuators=['stateled6']).getDict())
        roomDB.insert(Room(key='room7',maxStaff=3,sensors=['sensor11', 'sensor12'], actuators=['stateled7']).getDict())
        roomDB.insert(Room(key='room8',maxStaff=3,sensors=['sensor13', 'sensor14'], actuators=['stateled8']).getDict())
        roomDB.insert(Room(key='room9',maxStaff=3,sensors=['sensor15', 'sensor16'], actuators=['stateled9']).getDict())
        roomDB.insert(Room(key='room10',maxStaff=3,sensors=['sensor17', 'sensor18'], actuators=['stateled10']).getDict())
        for i in range(41):
            usersDB.insert(User(key='staff' + str(i)).getDict())
        self._setSensorRooms()
        self._setActuatorRooms()
