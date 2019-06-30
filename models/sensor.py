class Sensor():
    def __init__(self, key, data={}, room=''):
        self.key = key
        self.data = data
        self.room = room

    def getSensor(self):
        return {'key': self.key,
                'data': self.data,
                'room': self.room}