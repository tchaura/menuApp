from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
import os
from .models import db
from .models import MenuItem, Subcategory, Information
from .pillow import compress
from .utils import rename_static_files, change_lang_code
from .constants import STATIC_PATH, MAIN_SITE_URL, APP_ROOT_FOLDER_PATH

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')

# first lang is the primary
app.config['LANGUAGES'] = {
    'en': 'English',
    'ge': 'Georgian',
    'tr': 'Turkish',
    'ar': 'Arabian',
    'fa': 'Farsi',
    'ru': 'Russian'
}

app.config['STATIC_PATH'] = STATIC_PATH
app.config['MAIN_SITE_URL'] = MAIN_SITE_URL

app.config['DEFAULT_LANG'] = list(app.config['LANGUAGES'].keys())[0]
login_manager = LoginManager(app)

from . import admin
from . import localization
from . import index
from . import routes
from . import login

db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = os.environ.get("MENU_APP_SECRET_KEY")

db.init_app(app)


def get_locale():
    return app.config['DEFAULT_LANG']


babel = Babel(app, locale_selector=get_locale)


def compress_all():
    # compress all photos in Subcategory and MenuItem
    menu_items = MenuItem.query.all()
    for item in menu_items:
        if os.path.exists(APP_ROOT_FOLDER_PATH + item.item_photo):
            compress(APP_ROOT_FOLDER_PATH + item.item_photo)
    subcategories = Subcategory.query.all()
    for item in subcategories:
        if os.path.exists(APP_ROOT_FOLDER_PATH + item.subcategory_photo):
            compress(APP_ROOT_FOLDER_PATH + item.subcategory_photo)


with app.app_context():
    db.create_all()

    # renames all static files according to their associated row id in database
    # rename_static_files(db)

    # change language code
    # change_lang_code(db, "zh", "cn")



