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

    def updateSensorData(self, key, data):
        sensorQuery = Query()
        sensorsDB.upsert({'key': key, 'data': data }, sensorQuery.key == key)

    def updateSensorRoom(self, key, room):
        sensorQuery = Query()
        sensorsDB.update({'room': room }, sensorQuery.key == key)

    def getRoomData(self, room):
        roomQuery = Query()
        sensorQuery = Query()
        sensorData = []
        sensors = roomDB.get(where('room')==room)['sensors']
        for sensor in sensors:
            sensorData.append(sensorsDB.get(where('key') == sensor)['data'])
    def _initialisation(self):
        sensorsDB.insert(Sensor(key='multisensor_Temperature').getSensor())
        '''roomDB.insert(Room('room1',5,['sensor1', 'sensor2','sensor3']).getRoom())
        roomDB.insert(Room('room2',3,['sensor4', 'sensor5','sensor6']).getRoom())
        usersDB.insert(User('staff1', []).getUser())
        usersDB.insert(User('staff2', []).getUser())
        usersDB.insert(User('staff3', []).getUser())
        usersDB.insert(User('staff4', []).getUser())
        usersDB.insert(User('staff5', []).getUser())
        usersDB.insert(User('staff6', []).getUser())
        usersDB.insert(User('staff7', []).getUser())
        sensorsDB.insert(Sensor(key='sensor1', room='room1').getSensor())
        sensorsDB.insert(Sensor(key='sensor2', room='room1').getSensor())
        sensorsDB.insert(Sensor(key='sensor3', room='room1').getSensor())
        sensorsDB.insert(Sensor(key='sensor4', room='room2').getSensor())
        sensorsDB.insert(Sensor(key='sensor5', room='room2').getSensor())
        sensorsDB.insert(Sensor(key='sensor6', room='room2').getSensor())
'''
