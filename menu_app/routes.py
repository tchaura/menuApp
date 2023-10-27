import json
import re
from unicodedata import category
from menu_app import app
from flask import jsonify, render_template, request, session, redirect
from menu_app.models import (get_menu_items_by_subcategory_id, get_subcategories_by_category_id)

@app.route("/categories")
def get_categories_json():
    category_id = request.values['category_id']
    subcategories = get_subcategories_by_category_id(category_id)
    subcategory_data = [{"subcategory_id": subcategory.subcategory_id, "subcategory_name": subcategory.subcategory_name, "subcategory_photo": subcategory.subcategory_photo} for subcategory in subcategories]
    return jsonify({ 'subcategories' : subcategory_data})

@app.route("/menu_items")
def get_menu_items_json():
    subcategory_id = request.values['subcategory_id']
    menu_items = get_menu_items_by_subcategory_id(subcategory_id)
    menu_item_data = [{"item_id": item.item_id, "item_name": item.item_name, "price": item.price, "description": item.description, "ingredients": item.ingredients, "weight": item.weight, "item_photo": item.item_photo} for item in menu_items]    
    return jsonify({ 'menu_items' : menu_item_data })

@app.route('/set_language/<language>')
def set_language(language):
    session['locale'] = language
    return redirect(request.referrer)
