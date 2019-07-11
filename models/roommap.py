class Roommap():
    def __init__(self, datum, room='' , users=[], active=False):
        self._datum = datum
        self._room = room
        self._users = users
        self._active = active

    def getDict(self):
        return {'datum': self._datum,
                'room': self._room,
                'users': self._users,
                'active': self._active}