from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
import os
from .models import db
from .models import MenuItem, Subcategory
from .pillow import compress



app = Flask(__name__)

app.config['LANGUAGES'] = {
    'en': 'English',
    'ru': 'Русский',
    'tr': 'Türkçe',
    'zh': '中文'
}
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
    return 'ru'

babel = Babel(app, locale_selector = get_locale)

with app.app_context():
    db.create_all()
    
    # compress all photos in Subcategory and MenuItem
    # menu_items = MenuItem.query.all()
    # for item in menu_items:
    #     if os.path.exists('menu_app/' + item.item_photo):
    #         compress('menu_app/' + item.item_photo)
    # subcategories = Subcategory.query.all()
    # for item in subcategories:
    #     if os.path.exists('menu_app/' + item.subcategory_photo):
    #         compress('menu_app/' + item.subcategory_photo)