import datetime
from flask import (
    render_template, request
)

from .models import (Category, Information, Popup)
from .localization import get_translated_model

from . import app, db


@app.route("/", methods = ['GET', 'POST'])
def index():
    info = Information.query.first()
    if info:
        app.config['SITE_NAME'] = Information.query.first().title
    categories = Category.query.all()

    popup_config = {}
    popup = db.session.query(Popup).first()
    popup_is_shown = request.cookies.get('popup_is_shown')
    popup_config['show'] = popup and (popup.show and popup.popup_img and (not popup_is_shown or popup.show_always))
    if popup:
        popup_config['background_click'] = popup.background_click
        popup_config['close_timeout'] = popup.close_timeout

    lang = request.cookies.get('lang')

    args = {
        'categories': categories,
        'info': info,
        'year': datetime.datetime.now().year,
        'popup_config': popup_config
    }

    if lang == app.config['DEFAULT_LANG'] or not lang:
        return render_template("subcategories.html", **args)

    translated_categories = get_translated_model(Category, lang)
    translated_info = get_translated_model(Information, lang, 'info_id')

    args['categories'] = translated_categories if translated_categories else categories
    args['info'] = translated_info[0] if translated_info else info

    return render_template('subcategories.html', **args)
        