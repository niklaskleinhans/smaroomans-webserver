class User():
    def __init__(self, key, workplan = []):
        self.key = key
        self.workplan = workplan

    def getDict(self):
        return {'key': self.key,
                'workplan': self.workplan}