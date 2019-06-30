class Room():
    def __init__(self, key, maxStaff=0, sensors=[]):
        self._key = key
        self._maxStaff = maxStaff
        self._sensors = sensors

    def getRoom(self):
        return {'key': self._key,
                'maxStaff': self._maxStaff,
                'sensors': self._sensors}
    