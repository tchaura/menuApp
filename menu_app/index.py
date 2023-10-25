from audioop import add
from crypt import methods
import re
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from menu_app.db import get_db

bp = Blueprint('subcategories', __name__)

@bp.route("/", methods = ['GET', 'POST'])
def index():
    db = get_db()
    categories = db.execute(
        'SELECT category_id, category_name'
        ' FROM Categories'
    ).fetchall()
    
    # add_subcategory()
    
    if request.method == 'POST':
        subcategory_id = request.form.get('subcategory')
        menu_items = get_menu_items(subcategory_id)
        
        return render_template("menu_items.html", menu_items = menu_items, categories = categories)
        # return str(menu_items[0]['item_name'])
    
    subcategories = get_subcategories(categories[0]['category_id'])
    
    return render_template("subcategories.html", categories = categories, subcategories = subcategories)

def get_subcategories(id):
    db = get_db()
    subcategories = db.execute(
        'SELECT Subcategories.subcategory_id, Subcategories.subcategory_name, Subcategories.subcategory_photo'
        ' FROM Categories'
        ' JOIN Subcategories ON Categories.category_id = Subcategories.category_id'
        ' WHERE Categories.category_id = ?', (id, )
        ).fetchall()
    return subcategories

def get_menu_items(id):
    db = get_db()
    menu_items = db.execute(
        'SELECT item_id, item_name, price, description, ingredients, weight, item_photo, subcategory_name'
        ' FROM Subcategories'
        ' JOIN MenuItems ON MenuItems.subcategory_id = Subcategories.subcategory_id'
        ' WHERE Subcategories.subcategory_id = ?', (id, )
    ).fetchall()
    
    return menu_items

def add_subcategory():
    with open('menu_app/static/img/header.jpg', 'rb') as f:
        blob_data = f.read()
        
        db = get_db()
        db.execute("INSERT INTO Subcategories (subcategory_name, category_id, photo) VALUES (?, ?, ?)",
               ("Выпечка", 1, blob_data))  # Пример для загрузки BLOB-файла в таблицу
        db.commit()
        f.close()
