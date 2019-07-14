'''
Room structure
'''


class Room():
    def __init__(self, key, active=True, notifications=[], maxStaff=0, sensors=[], actuators=[], users=[], _id=0):
        self._key = key
        self._maxStaff = maxStaff
        self._sensors = sensors
        self._actuators = actuators
        self._active = active
        self._notifications = notifications
        self._users = users

    def getDict(self):
        '''
        returns model as dict
        '''
        return {'key': self._key,
                'maxStaff': self._maxStaff,
                'sensors': self._sensors,
                'actuators': self._actuators,
                'active': self._active,
                'notifications': self._notifications,
                'users': self._users}
