class Room():
    def __init__(self, name, maxStaff=0, sensors=[]):
        self._name = name
        self._maxStaff = maxStaff
        self._sensors = sensors

    def getRoom(self):
        return {'name': self._name,
                'maxStaff': self._maxStaff,
                'sensors': self._sensors}
    