class User():
    def __init__(self, name, workplan = []):
        self.name = name
        self.workplan = workplan

    def getUser(self):
        return {'name': self.name,
                'workplan': self.workplan}