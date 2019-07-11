class Notification():
    def __init__(self, notificationType, text, topic='', topicdata=''):
        self._text = text
        self._topic = topic
        self._topicdata = topicdata
        self._notificationType = notificationType

    def getDict(self):
        return {'text': self._text,
                'topic': self._topic,
                'topicdata': self._topicdata,
                'notificationType': self._notificationType}
