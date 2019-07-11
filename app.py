from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from flask_mqtt import Mqtt
import json

from threads.stopableThread import StopableThread
from database.database import DB
from external.sensormanager.sensormanager import SensorManager
from utilities.roommanger import RoomManager
import utilities.util as util
from errorhandling.errortypes import NotModified, DBError
from utilities.statemachine import StateMachine

brokerIP = '192.168.1.230'
test = {"mac":"", "cmd": "switch", "val": "on"}

app = Flask(__name__,
            static_url_path = '',
            template_folder = "../smaroomans-client/dist/")

app.config['MQTT_BROKER_URL'] = '192.168.1.230'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds

myDB = DB(app)
mqtt = Mqtt(app)
sensorManager = SensorManager(myDB, brokerIP, mqtt)
statemachine = StateMachine(myDB,sensorManager)
statemachineThread = StopableThread(name="statemachineThread", function= statemachine.checkConditions, args={}) 
statemachineThread.start()
roomManager = RoomManager(myDB, sensorManager)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@mqtt.on_connect()
def handle_connect(client,userdata,flags,rc):
    sensorManager.on_connect(client,userdata,flags,rc)
    sensorManager.subscriber.startSubscription()

@mqtt.on_disconnect()
def handle_disconnect(client,userdata,rc):
    sensorManager.on_disconnect(client,userdata,rc)

@mqtt.on_message()
def handle_mqtt_message(client, userdata,message):
    sensorManager.subscriber.on_message(client,userdata,message) 

@app.errorhandler(NotModified)
def handle_not_modified(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(DBError)
def handle_DBError(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('../smaroomans-client/dist/', 'favicon.ico')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../smaroomans-client/dist/js/', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../smaroomans-client/dist/css/', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('../smaroomans-client/dist/fonts/', path)

@app.route("/api/triggernotification", methods=['POST'])
def triggerNotification():
    print(request.method)
    result = request.json
    test['val']= result['val']
    sensorManager.publisher.publish('plugwise2py/cmd/switch/000D6F0004B1E6C4', test)
    return '',status.HTTP_200_OK

@app.route('/api/stop', methods=['PUT'])
def stopThread():
    sensorManager.stopSubscription()
    return '', status.HTTP_200_OK

@app.route('/api/start', methods=['PUT'])
def startThread():
    sensorManager.startSubscription()
    return '', status.HTTP_200_OK

@app.route('/api/initdb', methods=['PUT'])
def initDB():
    myDB._initialisation()    
    return '', status.HTTP_200_OK

@app.route('/api/allrooms', methods=['GET'])
def getRooms():
    try:
        result=[]
        for room in myDB.getAllRooms():
            result.append({ 'key': room['key'], 
                            'sensors': room['sensors'],
                            'active' : room['active'],
                            'users' : room['users']})
    except Exception as e:
        raise DBError(str(e), status_code=500) 
    return jsonify({'rooms': result})

@app.route('/api/roomsensors/<string:roomkey>', methods=['GET'])
def getRoomSensors(roomkey):
    try:
        sensors = myDB.getRoomSensors(roomkey)
    except Exception as e:
        raise DBError(str(e), status_code=500) 
    return jsonify({'sensors': sensors})

@app.route('/api/allusers', methods=['GET'])
def getAllUsers():
    try:
        result=[]
        for user in myDB.getAllUsers():
           result.append({'key' : user['key'], 'workplan': user['workplan']})
    except Exception as e:
        raise DBError(str(e), status_code=500) 
    return jsonify({'users': result})

#@app.route('/api/getuserplan', methods=['GET'])

@app.route('/api/setuserplan', methods=['PUT'])
def setUserPlan():
    payload = request.json
    try:
        myDB.setUserPlan(payload['key'], payload['workplan'])
        roomManager.optimizeRoomMaps()
    except Exception as e:
        raise NotModified(str(e), status_code=304)
    return '', status.HTTP_200_OK


@app.route('/api/getroommaps', methods=['GET'])
def getRoomMaps():
    try:
        result=[]
        for roommap in roomManager.checkRoomManagerEntrys():
            result.append({'datum': util.secondsToDatum(roommap['datum']), 'room': roommap['room'], 'users': roommap['users']})
    except Exception as e:
        raise NotModified(str(e), status_code=304)
    return jsonify({'data' : result})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
