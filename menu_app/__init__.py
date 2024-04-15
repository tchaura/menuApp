from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
import os
from .models import db
from .models import MenuItem, Subcategory, Information
from .pillow import compress

app = Flask(__name__)

# first lang is the primary
app.config['LANGUAGES'] = {
    'en': 'English',
    'ge': 'ქართული',
    'tr': 'Türkçe',
    'he': 'עִברִית',
    'ru': 'Русский',
}

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
        if os.path.exists('menu_app/' + item.item_photo):
            compress('menu_app/' + item.item_photo)
    subcategories = Subcategory.query.all()
    for item in subcategories:
        if os.path.exists('menu_app/' + item.subcategory_photo):
            compress('menu_app/' + item.subcategory_photo)


# renames all static files according to their associated row id in database
def rename_static_files():
    menu_items = MenuItem.query.filter(MenuItem.item_photo != "")
    renamed_files = set()
    for item in menu_items:
        rename_file(item, renamed_files)


def rename_file(item, renamed_files):
    cur_path = item.item_photo

    if cur_path is None:
        return
    if not os.path.exists('menu_app/' + cur_path):
        item.item_photo = ""
        return
    file_extension = os.path.splitext(cur_path)[1]
    target_path = os.path.join('static/img/menu_items/', str(item.item_id) + file_extension)

    if cur_path == target_path:
        renamed_files.add(target_path)
        return

    if cur_path in renamed_files:
        item.item_photo = ""
        return

    if os.path.exists('menu_app/' + target_path):
        while db.session.query(MenuItem.query.filter(MenuItem.item_photo == target_path).exists()).scalar():
            conflicting_item = MenuItem.query.filter(MenuItem.item_photo == target_path).first()
            rename_file(conflicting_item, renamed_files)

    os.rename('menu_app/' + cur_path, 'menu_app/' + target_path)
    item.item_photo = target_path
    db.session.commit()

    renamed_files.add(target_path)


with app.app_context():
    db.create_all()


