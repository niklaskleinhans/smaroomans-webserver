from tinydb import TinyDB, Query, where
from models.room import Room
from models.user import User
from models.sensor import Sensor
import numpy as np

roomDB = TinyDB('database/content/room.json')
usersDB = TinyDB('database/content/users.json')
sensorsDB = TinyDB('database/content/sensors.json')
organizerDB = TinyDB('database/content/organizer.json')

class DB():
    def __init__(self):
        print('init DB')
    
    def getAllRooms(self):
        return roomDB.all()
    
    def getAllSensors(self):
        return sensorsDB.all()

    def updateSensorData(self, key, data):
        key = str(key).replace(" ","_")
        sensorQuery = Query()
        sensor = sensorsDB.get(where('key')==key)
        if sensor is not None:
            sensorsDB.upsert({'key': key, 'data': data }, sensorQuery.key == key)
        else:
            sensorsDB.upsert(Sensor(key=key,data=data).getSensor(), sensorQuery.key == key)

    def updateSensorRoom(self, key, room):
        sensorQuery = Query()
        sensorsDB.update({'room': room }, sensorQuery.key == str(key).replace(" ", "_"))

    def getSensorTopic(self, key):
        key = str(key).replace(" ", "_")
        sensor = sensorsDB.get(where('key')==key)
        if sensor is not None:
            topic='sensor'
            if not sensor['room'] == "" :  
                topic= topic+"/"+sensor['room']
            topic = topic+"/"+str(key)
            return topic
        else:
            return None

    def getSensorData(self, key):
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

    def setSensorRooms(self):
        sensors = self.getAllSensors()
        sensorQuery=Query()
        rooms = self.getAllRooms()
        for sensor in sensors:
            for room in rooms:
                if sensor['key'] in room['sensors']:
                    sensorsDB.update({'key': sensor['key'], 'room': room['key'] }, sensorQuery.key == sensor['key'])

    def _initialisation(self):
        roomDB.purge_tables()
        usersDB.purge_tables()
        roomDB.insert(Room('room1',5,['multisensor_Relative_Humidity', 'multisensor_Temperature','multisensor_Ultraviolet', 'multisensor_Group_1_Interval']).getRoom())
        roomDB.insert(Room('room2',3,['sensor4', 'sensor5','sensor6']).getRoom())
        usersDB.insert(User('staff1', []).getUser())
        usersDB.insert(User('staff2', []).getUser())
        usersDB.insert(User('staff3', []).getUser())
        usersDB.insert(User('staff4', []).getUser())
        usersDB.insert(User('staff5', []).getUser())
        usersDB.insert(User('staff6', []).getUser())
        usersDB.insert(User('staff7', []).getUser())
        self.setSensorRooms()
