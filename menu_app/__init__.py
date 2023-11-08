from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
import os
from .models import db



app = Flask(__name__)

app.config['LANGUAGES'] = {
    'en': 'English',
    'ru': 'Русский',
    'tr': 'Türkçe',
    'zh': '中文'
}
login_manager = LoginManager(app)
import menu_app.admin
import menu_app.localization
from . import index

import menu_app.routes


import menu_app.login

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = os.environ.get("MENU_APP_SECRET_KEY")

db.init_app(app)
app.register_blueprint(index.bp)

def get_locale():
    return 'ru'

babel = Babel(app, locale_selector = get_locale)
