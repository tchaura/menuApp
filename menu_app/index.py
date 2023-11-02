from audioop import add
from crypt import methods
from flask_babel import gettext
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from flask_babel import get_locale

from menu_app.models import (get_all_categories, get_menu_items_by_subcategory_id, get_subcategories_by_category_id)

bp = Blueprint('subcategories', __name__)

@bp.route("/", methods = ['GET', 'POST'])
def index():
    categories = get_all_categories()
    locale = get_locale()
    test = gettext("This isn't working")
    flash(test)
        
    return render_template("subcategories.html", categories = categories, locale = locale)