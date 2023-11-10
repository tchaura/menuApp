import datetime
import re
from flask import (
    Blueprint, render_template, request
)

from .models import (Category, Information, Translation)
from .localization import get_translated_model

from . import app

@app.route("/", methods = ['GET', 'POST'])
def index():
    info = Information.query.first()
    categories = Category.query.all()
    lang = request.cookies.get('lang')
    if lang == 'ru' or not lang:
        return render_template("subcategories.html", categories = categories, info = info, year = datetime.date.today().year)
    
    translated_categories = get_translated_model(Category, lang)
    translated_info = get_translated_model(Information, lang, 'info_id')
    
    return render_template('subcategories.html', categories = translated_categories if translated_categories else categories, info = translated_info[0] if translated_info else info, year = datetime.date.today().year)
        