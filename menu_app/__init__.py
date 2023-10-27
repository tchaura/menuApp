from http import cookies
from flask import Flask, render_template, request, session
from flask_babel import Babel
from flask_login import LoginManager
from .models import db
import os
from . import index


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
babel = Babel(app)
login_manager = LoginManager(app)
import menu_app.routes
import menu_app.models
import menu_app.admin


import menu_app.login

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = os.environ.get("MENU_APP_SECRET_KEY")
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'

db.init_app(app)
app.register_blueprint(index.bp)


# with app.app_context():
#     db.create_all()
