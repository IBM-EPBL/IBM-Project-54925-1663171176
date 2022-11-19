from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import abort

app = Flask(__name__)

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/index")

@app.route("/Display.html", methods = ["GET", "POST"] )

def register():
    if request.method == "POST":
        name = request.form['name']
        mail = request.form['mail']
        
        if name == "Admin":
            return redirect(url_for("about"))
        elif name == "Dummy":
            abort(403)
        else:
            return render_template("Display.html", name = name, mail = mail)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug = True)
