class Room():
    def __init__(self, key, active=True, maxStaff=0, sensors=[], actuators=[]):
        self._key = key
        self._maxStaff = maxStaff
        self._sensors = sensors
        self._actuators = actuators
        self._active = active

    def getDict(self):
        return {'key': self._key,
                'maxStaff': self._maxStaff,
                'sensors': self._sensors,
                'actuators': self._actuators,
                'active': self._active}
    