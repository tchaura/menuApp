from . import app
from .localization import get_translated_model
from flask_babel import refresh
from flask import g, jsonify, request, session, redirect
from .models import (Category, MenuItem, Subcategory)

@app.route("/categories")
def get_subcategories_json():
    category_id = request.values['category_id']
    lang = request.cookies.get('lang')
    has_subcategories = Category.query.filter(Category.category_id == category_id).first().has_subcategories
    if has_subcategories == 0:
        return jsonify({'has_subcategories' : bool(has_subcategories)})
    if lang == app.config['DEFAULT_LANG']:
        subcategories = Subcategory.query.filter(Subcategory.category_id == category_id)
        subcategory_data = [{"subcategory_id": subcategory.subcategory_id, "subcategory_name": subcategory.subcategory_name, "subcategory_photo": subcategory.subcategory_photo} for subcategory in subcategories]
        return jsonify({ 'subcategories' : subcategory_data})
    
    translated_model = get_translated_model(Subcategory, lang)
    
    filtered_model = list(filter(lambda row: row['category_id'] == int(category_id), translated_model))
    
    return jsonify({'subcategories': filtered_model})
    

@app.route("/get_first_category_id")
def get_first_category_id():
    first_category = Category.query.first()
    category_id = first_category.category_id if first_category else 0
    return jsonify({'category_id' : category_id})
    

@app.route("/menu_items")
def get_menu_items_json():
    category_id = request.values['category_id']
    subcategory_id = request.values['subcategory_id']
    lang = request.cookies.get('lang')
    parent_category_id = Subcategory.query.filter(Subcategory.subcategory_id == subcategory_id).first().category_id if subcategory_id else 1
    
    if lang == app.config['DEFAULT_LANG']:
        menu_items = MenuItem.query.filter(MenuItem.category_id == category_id if category_id else MenuItem.subcategory_id == subcategory_id)
        menu_item_data = [{"item_id": item.item_id, "item_name": item.item_name, "price": item.price, "description": item.description, "ingredients": item.ingredients, "weight": item.weight, "item_photo": item.item_photo, "measure_unit": item.measure_unit} for item in menu_items]
        return jsonify({'menu_items': menu_item_data, 'parent_category_id': parent_category_id})

    translated_model = get_translated_model(MenuItem, lang, 'item_id')
    if category_id:
        filtered_model = list(filter(lambda row: row['category_id'] == int(category_id), translated_model))
    else:
        filtered_model = list(filter(lambda row: row['subcategory_id'] == int(subcategory_id), translated_model))

    return jsonify({'menu_items': filtered_model, 'parent_category_id': parent_category_id})

@app.route('/set_language/<lang>')
def set_language(lang):
    session['lang'] = lang
    refresh()
    return redirect('/')

@app.route('/search')
def search():
    query = request.values['query']
    menu_items = MenuItem.query.all()
    menu_item_data = [{"item_id": item.item_id, "item_name": item.item_name, "price": item.price, "description": item.description, "ingredients": item.ingredients, "weight": item.weight, "item_photo": item.item_photo} for item in menu_items]  
    search_data = list(filter(lambda item : query in item['item_name'].lower(), menu_item_data))
    return jsonify({'menu_items': search_data})


@app.before_request
def before_request():
    lang = session.get('lang') or request.cookies.get('lang')
    if lang:
        g.locale = lang
