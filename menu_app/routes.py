import json
import re
from unicodedata import category
from menu_app import app
from flask import jsonify, render_template, request
from menu_app.db import get_db
from menu_app.index import get_menu_items, get_subcategories

@app.route("/categories")
def get_categories_json():
    category_id = request.values['category_id']
    subcategories = get_subcategories(category_id)
    subcategories_data = []
    for subcategory in subcategories:
        subcategory_id, subcategory_name, photo = subcategory
        subcategory_dict = {
            "subcategory_id": subcategory_id,
            "subcategory_name": subcategory_name,
            "photo": photo
        }
        subcategories_data.append(subcategory_dict)
    return jsonify({ 'subcategories' : subcategories_data})

@app.route("/menu_items")
def get_menu_items_json():
    subcategory_id = request.values['subcategory_id']
    menu_items = get_menu_items(subcategory_id)
    menu_items_data = []
    for item in menu_items:
        item_id, item_name, price, description, ingredients, weight, item_photo, subcategory_name = item
        menu_item_dict = {
            "item_id": item_id,
            "item_name": item_name,
            "price": price,
            "description": description,
            "ingredients": ingredients,
            "weight": weight,
            "photo": item_photo,
            "subcategory_name": subcategory_name
        }
        menu_items_data.append(menu_item_dict)
    
    return jsonify({ 'menu_items' : menu_items_data })