from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from flask_mqtt import Mqtt
import json

from database.database import DB
from external.sensormanager.sensormanager import SensorManager
myDB = DB()
#myDB._initialisation()
#sensorManager = SensorManager(myDB)

test = {"mac":"", "cmd": "switch", "val": "on"}

app = Flask(__name__,
            static_url_path = '',
            template_folder = "../smaroomans-client/dist/")

app.config['MQTT_BROKER_URL'] = '192.168.1.230'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

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

@app.route("/api/triggernotification", methods=['POST'])
def triggerNotification():
    print(request.method)
    result = request.json
    test['val']= result['val']
    mqtt.publish('plugwise2py/cmd/switch/000D6F0004B1E6C4', json.dumps(test))
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
    return jsonify({'rooms': myDB.getAllRooms()})

@app.route('/api/roomsensors/<string:roomkey>', methods=['GET'])
def getRoomSensors(roomkey):
    sensors = myDB.getRoomSensors(roomkey)
    #print(roomkey)
    return jsonify({'sensors': sensors})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
