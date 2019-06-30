class Actuator():
    def __init__(self, key, sensortype, data={}, room=''):
        self.key = key
        self.data = data
        self.room = room
        self.sensortype = sensortype

    def getDict(self):
        return {'key': self.key,
                'data': self.data,
                'room': self.room,
                'sensortype': self.sensortype}