from http import cookies
from flask import Flask, render_template, request, session
from flask_babel import Babel, refresh
from flask_login import LoginManager
import os
from .models import db
from . import index
from flask import g


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

login_manager = LoginManager(app)
import menu_app.models
import menu_app.admin

import menu_app.routes


import menu_app.login

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = os.environ.get("MENU_APP_SECRET_KEY")

db.init_app(app)
app.register_blueprint(index.bp)

app.config['LANGUAGES'] = {
    'en': 'English',
    'ru': 'Русский',
    'tr': 'Türkçe',
    'zh': '中文'
}
def get_locale():
    return 'ru'
    # return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

babel = Babel(app, locale_selector = get_locale)