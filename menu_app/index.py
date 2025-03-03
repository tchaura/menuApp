from posixpath import join as urljoin
from typing import Type

from flask import (
    render_template, request, make_response
)

from .models import (Category, Information, Popup, Subcategory)
from .localization import get_translated_model
import menu_app.constants as constants

from . import app, db, MenuItem


@app.route("/", methods = ['GET', 'POST'])
def index(redirect_type: Type[db.Model] = None, redirect_id: int = None, **kwargs):
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

    lang = request.args.get('lang') or kwargs.get('lang') or request.cookies.get('lang')

    is_valid_redirect = (redirect_type is not None
                         and (redirect_type in [Category, Subcategory, MenuItem])
                         and redirect_id is not None)

    args = {
        'popup_config': popup_config,
    }

    if not lang or lang == app.config['DEFAULT_LANG'] or lang not in app.config['LANGUAGES'].keys():
        args['categories'] = categories
        args['info'] = info
        lang = app.config['DEFAULT_LANG']
    else:
        translated_categories = get_translated_model(Category, lang)
        translated_info = get_translated_model(Information, lang, 'info_id')
        args['categories'] = translated_categories if translated_categories else categories
        args['info'] = translated_info[0] if translated_info else info

    # redirect currently working with category type only :(
    if is_valid_redirect and redirect_type is Category:
        enrich_category_with_redirect(args['categories'], redirect_id)

    args['site_url'] = urljoin(constants.MAIN_SITE_URL, constants.MAIN_SITE_LOCALE_PATHS.get(lang) or "") \
        if constants.MAIN_SITE_URL else ""

    response = make_response(render_template('subcategories.html', **args))
    response.set_cookie('lang', lang)
    return response


def enrich_category_with_redirect(categories: list[Category] | list[dict], category_id: int):
    for i, item in enumerate(categories):
        if type(item) is dict:
            if item['category_id'] == category_id:
                item['redirect'] = True
        else:
            if item.category_id == category_id:
                item.redirect = True

        categories[i] = item
