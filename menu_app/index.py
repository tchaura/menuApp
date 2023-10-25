from audioop import add
from crypt import methods
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from menu_app.db import get_db

from menu_app.models import (get_all_categories, get_menu_items_by_subcategory_id, get_subcategories_by_category_id)

bp = Blueprint('subcategories', __name__)

@bp.route("/", methods = ['GET', 'POST'])
def index():
    db = get_db()
    categories = get_all_categories()
        
    return render_template("subcategories.html", categories = categories)