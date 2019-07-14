'''
Sensor structure
'''


class Sensor():
    def __init__(self, key, topic='', sensortype='', data={}, room='', name=''):
        self._key = key
        self._data = data
        self._room = room
        self._sensortype = sensortype
        self._topic = topic
        self._name = name

    def getDict(self):
        '''
        returns model as dict
        '''
        return {'key': self._key,
                'data': self._data,
                'room': self._room,
                'sensortype': self._sensortype,
                'topic': self._topic,
                'name': self._name}
