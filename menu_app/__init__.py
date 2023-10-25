from flask import Flask, render_template
from flask_babel import Babel
import os

app = Flask(__name__)
babel = Babel(app)
BABEL_DEFAULT_LOCALE = "ru"

from . import db
db.init_app(app)

app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

import menu_app.routes
import menu_app.db

from . import index
app.register_blueprint(index.bp)
app.add_url_rule('/', endpoint='index')