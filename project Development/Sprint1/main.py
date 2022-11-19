from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import abort

app = Flask(__name__)

@app.route("/")

def home():
    return render_template("Display.html")


if __name__ == '__main__':
    app.run(debug = True)
