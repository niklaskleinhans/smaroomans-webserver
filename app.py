from flask import Flask, render_template

app = Flask(__name__,
            static_folder = "../smaroomans-client/dist/static",
            template_folder = "../smaroomans-client/dist")

@app.route('/')
def index():
    return render_template("index.html")