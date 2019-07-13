'''
roommanger to optimize user room mapping
'''

from models.roommap import Roommap
import datetime


class RoomManager():
    def __init__(self, database, sensorManager):
        print("init Roommanger")
        self.DB = database
        self.sensorManager = sensorManager

    def checkRoomManagerEntrys(self):
        """
        returns all Room User Mapping entry in the next 30 days

        Returns
        -------
        mongodb.cursors
            containing all room user mapping entrys in the next 30 days
        """
        roommaps = self.DB.getRoomMapsByDatum(datetime.datetime.now().strftime("%Y-%m-%d"),
                                              (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d"))
        return roommaps

    def optimizeRoomMaps(self):
        """
        starts the room user mapping optimization.
        Directly updates the Database and sets the Room leds
        """
        relevantDates = [(datetime.datetime.now(
        ) + datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(31)]

        for date in relevantDates:
            relevantUsers = [
                user for user in self.DB.getAllUsers() if date not in user['workplan']]
            for room in self.DB.getAllRooms():
                roomUsers = []
                currentUserCount = 0
                while currentUserCount < room['maxStaff']:
                    if len(relevantUsers) == 0:
                        break
                    roomUsers.append(relevantUsers.pop(0)['key'])
                    currentUserCount += 1
                if len(roomUsers) == 0:
                    state = False
                else:
                    state = True
                self.DB.updateRoomMap(
                    Roommap(datum=date, room=room['key'], users=roomUsers, active=state).getDict())
                if date == datetime.datetime.now().strftime('%Y-%m-%d'):
                    self.sensorManager.publisher.publish(
                        'actuator/stateled', {'room': room['key'], 'state': int(state)})
