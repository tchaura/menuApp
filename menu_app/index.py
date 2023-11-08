import datetime
from flask import (
    Blueprint, render_template, request
)

from menu_app.models import (Category, Information, Translation)
from menu_app.localization import get_translated_model

bp = Blueprint('subcategories', __name__)

@bp.route("/", methods = ['GET', 'POST'])
def index():
    info = Information.query.first()
    categories = Category.query.all()
    lang = request.cookies.get('lang')
    if lang == 'ru':
        return render_template("subcategories.html", categories = categories, info = info, year = datetime.date.today().year)
    
    translated_categories = get_translated_model(Category, lang)
    translated_info = get_translated_model(Information, lang, 'info_id')
    
    return render_template('subcategories.html', categories = translated_categories, info = translated_info[0], year = datetime.date.today().year)
        