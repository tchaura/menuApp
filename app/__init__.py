from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)
BABEL_DEFAULT_LOCALE = "ru"


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")