from models.notification import Notification
import time

class StateMachine():
    def __init__(self,database, publisher):
        self.DB=database = database
        self.publisher = publisher
        self.actionData = {}
        self.conditions= {'temperatureExceed': {'temperature': 25},
                          'temperatureBelow': {'temperature': 19},
                          'luminanceIsLow': {'luminance': 140}}
        self.triggers = [{'key' : 'sendOpenWindowNotification',
                         'actions' : [self.DB.addNotification, self.publisher.publishRoomNotifications],
                         'actiondata':[self.createNotificationOpenWindow, self.createPublishData],
                         'conditions': [self.temperatureExceed, self.windowOpen]},
                         {'key' : 'sendEnableLight',
                         'conditions' : [self.luminanceIsLow],
                         'actions' : [self.DB.addNotification, self.publisher.publishRoomNotifications],
                         'actiondata': [self.createNotificationEnableLight, self.createNoneData]}]


    def luminanceIsLow(self, room):
        try:
            if self.DB.getRoomLuminance(room) <= self.conditions['luminanceIsLow']['luminance']:
                return True
            else:
                return False 
        except Exception as e:
            print(e)

    def temperatureExceed(self, room):
        try:
            if self.DB.getRoomTemperature(room) >= self.conditions['temperatureExceed']['temperature']:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    
    def temperatureBelow(self, room):
        if self.DB.getRoomTemperature(room) < self.conditions['temperatureBelow']['temperature']:
            return True
        else:
            return False

    def windowOpen(self, room):
        if self.DB.getRoomWindowStatus(room) == 1:
            return True
        else:
            return False
    
    def windowClosed(self, room):
        if self.DB.getRoomWindowStatus(room) == 0:
            return True
        else:
            return False

    def createNoneData(self, room):
        return None

    def createPublishData(self, room):
        return None

    def createNotificationOpenWindow(self, room):
        return {'notification': Notification(notificationType='openwindow', text='Open Window').getDict(),
                'room': room}
    
    def createNotificationEnableLight(self, room):
        topic, topicdata = self.DB.getRoomActuatorTopicAndData(room, 'light')
        topicdata['val'] = 'on'
        return {'notification': Notification(notificationType='enableLight', text='Enable Light', topic=topic, topicdata=topicdata).getDict(),
                'room': room}
    
    def createNotificationDisbaleLight(self, room):
        topic, topicdata = self.DB.getRoomActuatorTopicAndData(room, 'light')
        topicdata['val'] = 'off'
        return {'notification': Notification(notificationType='enableLight', text='Enable Light', topic=topic, topicdata=topicdata).getDict(),
                'room': room}

    def checkConditions(self, stopfunction):
        while(not stopfunction()):
            time.sleep(10)
            for room in self.DB.getAllRooms():
                room = room['key']
                for trigger in self.triggers:
                    runCondition = True
                    for condition in trigger['conditions']:
                        runCondition = runCondition and condition(room)
                    if runCondition:
                        for idx, action in enumerate(trigger['actions']):
                            args = trigger['actiondata'][idx]
                            if args(room) is not None:
                                try:
                                    action(**trigger['actiondata'][idx](room))
                                except Exception as e:
                                    print(e)
                            else:
                                action()