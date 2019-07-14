'''
Actuator structure
'''


class Actuator():
    def __init__(self, key, actuatortype='', topic='', topicdata={}, room=''):
        self._key = key
        self._topic = topic
        self._topicdata = topicdata
        self._room = room
        self._actuatortype = actuatortype

    def getDict(self):
        '''
        returns model as dict
        '''
        return {'key': self._key,
                'topic': self._topic,
                'topicdata': self._topicdata,
                'room': self._room,
                'actuatortype': self._actuatortype}
