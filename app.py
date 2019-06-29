from flask import Flask, render_template, send_from_directory

app = Flask(__name__,
            static_url_path = '',
            template_folder = "../smaroomans-client/dist/")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../smaroomans-client/dist/js/', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../smaroomans-client/dist/css/', path)

app.run(host='0.0.0.0')