class Actuator():
    def __init__(self, key, actuatortype='', topic='', data={}, room=''):
        self._key = key
        self._data = data
        self._room = room
        self._actuatortype = actuatortype

    def getDict(self):
        return {'key': self._key,
                'data': self._data,
                'room': self._room,
                'actuatortype': self._actuatortype}