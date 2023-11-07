from flask import (
    Blueprint, render_template, request
)

from menu_app.models import (Category, Translation)
from menu_app.localization import get_translated_model

bp = Blueprint('subcategories', __name__)

@bp.route("/", methods = ['GET', 'POST'])
def index():
    categories = Category.query.all()
    lang = request.cookies.get('lang')
    if lang == 'ru':
        return render_template("subcategories.html", categories = categories)
    
    translated_model = get_translated_model(Category, lang)
    
    return render_template('subcategories.html', categories = translated_model)
        