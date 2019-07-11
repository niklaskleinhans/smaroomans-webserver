from models.notification import Notification
import time

class StateMachine():
    def __init__(self,database, sensormanager):
        self.DB=database = database
        self.sensormanager= sensormanager
        self.actionData = {}
        self.conditions= {'temperatureExceed': {'temperature': 25},
                          'temperatureBelow': {'temperature': 19},
                          'luminanceIsLow': {'luminance': 90},
                          'luminanceIsHigh': {'luminance' : 100}}
        self.triggers = [{'key' : 'sendOpenWindowNotification',
                         'actions' : [self.DB.appendNotification],
                         'actiondata':[self.createNotificationOpenWindow],
                         'conditions': [self.temperatureExceed, self.windowClosed]},
                         {'key' : 'sendEnableLight',
                         'conditions' : [self.luminanceIsLow, self.lightOff],
                         'actions' : [self.DB.appendNotification],
                         'actiondata': [self.createNotificationEnableLight]},
                         {'key' : 'sendDisableLight',
                         'conditions' : [self.luminanceIsHigh, self.lightOn],
                         'actions' : [self.DB.appendNotification],
                         'actiondata': [self.createNotificationDisableLight]} ]


    def luminanceIsLow(self, room):
        try:
            luminance = self.DB.getRoomLuminance(room)
            if luminance is not None and luminance <= self.conditions['luminanceIsLow']['luminance']:
                return True
            else:
                return False 
        except Exception as e:
            print(e)
    
    def luminanceIsHigh(self, room):
        try:
            luminance = self.DB.getRoomLuminance(room)
            if luminance is not None and luminance > self.conditions['luminanceIsHigh']['luminance']:
                return True
            else:
                return False 
        except Exception as e:
            print(e)

    def lightOn(self, room):
        try:
            lightState = self.DB.getRoomLightState(room)
            if lightState is not None and lightState == 'on':
                return True
            else:
                return False 
        except Exception as e:
            print(e)
    
    def lightOff(self, room):
        try:
            lightState = self.DB.getRoomLightState(room)
            if lightState is not None and lightState == 'off':
                return True
            else:
                return False 
        except Exception as e:
            print(e)

    def temperatureExceed(self, room):
        try:
            temperature = self.DB.getRoomTemperature(room)
            if temperature is not None and temperature >= self.conditions['temperatureExceed']['temperature']:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def temperatureBelow(self, room):
        temperature = self.DB.getRoomTemperature(room)
        if temperature is not None and temperature < self.conditions['temperatureBelow']['temperature']:
            return True
        else:
            return False

    def windowOpen(self, room):
        windowStatus = self.DB.getRoomWindowStatus(room)
        if windowStatus is not None and windowStatus  == 1:
            return True
        else:
            return False
    
    def windowClosed(self, room):
        windowStatus = self.DB.getRoomWindowStatus(room)
        if windowStatus is not None and windowStatus == 0:
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
        return {'notification': Notification(notificationType='enablelight', text='Enable Light', topic=topic, topicdata=topicdata).getDict(),
                'room': room}

    def createNotificationDisableLight(self, room):
        topic, topicdata = self.DB.getRoomActuatorTopicAndData(room, 'light')
        topicdata['val'] = 'off'
        return {'notification': Notification(notificationType='disablelight', text='Disable Light', topic=topic, topicdata=topicdata).getDict(),
                'room': room}

    def checkConditions(self, stopfunction):
        while(not stopfunction()):
            time.sleep(2)
            try:
                self.DB.clearAllNotifications()
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
            except Exception as e:
                print(e)
            self.sensormanager.publisher.publishRoomNotifications()