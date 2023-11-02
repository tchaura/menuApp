import json
import re
from menu_app import app
from flask_babel import refresh
from flask import g, jsonify, render_template, request, session, redirect
from menu_app.models import (Category, MenuItem, Subcategory, get_menu_items_by_subcategory_id, get_subcategories_by_category_id)

@app.route("/categories")
def get_subcategories_json():
    category_id = request.values['category_id']
    has_subcategories = Category.query.filter(Category.category_id == category_id).first().has_subcategories
    if has_subcategories == 0:
        return jsonify({'has_subcategories' : bool(has_subcategories)})
    subcategories = Subcategory.query.filter(Subcategory.category_id == category_id)
    subcategory_data = [{"subcategory_id": subcategory.subcategory_id, "subcategory_name": subcategory.subcategory_name, "subcategory_photo": subcategory.subcategory_photo} for subcategory in subcategories]
    return jsonify({ 'subcategories' : subcategory_data})

@app.route("/menu_items")
def get_menu_items_json():
    category_id = request.values['category_id']
    subcategory_id = request.values['subcategory_id']
    menu_items = MenuItem.query.filter(MenuItem.category_id == category_id if category_id else MenuItem.subcategory_id == subcategory_id)
    menu_item_data = [{"item_id": item.item_id, "item_name": item.item_name, "price": item.price, "description": item.description, "ingredients": item.ingredients, "weight": item.weight, "item_photo": item.item_photo} for item in menu_items]  
    parent_category_id = Subcategory.query.filter(Subcategory.subcategory_id == subcategory_id).first().category_id if subcategory_id else 1
    return jsonify({ 'menu_items' : menu_item_data , 'parent_category_id' : parent_category_id})


@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    refresh()
    return redirect('/')

@app.before_request
def before_request():
    lang = session.get('lang') or request.cookies.get('lang')
    if lang:
        g.locale = lang


