
from ast import Sub
from nis import cat
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'Categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True)

class Subcategory(db.Model):
    __tablename__ = 'Subcategories'
    subcategory_id = db.Column(db.Integer, primary_key=True)
    subcategory_name = db.Column(db.String, nullable=False)
    subcategory_photo = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'))
    items = db.relationship('MenuItem', backref='subcategory', lazy=True)
    
    @property
    def category_name(self):
        category_name = Category.query.filter(Category.category_id == self.category_id).first().category_name
        return category_name
    
    @property
    def photo_thumb(self):
        return Markup('<img height=\'50px\' src=\'/' + (self.subcategory_photo if self.subcategory_photo else '') + '\'>')

class MenuItem(db.Model):
    __tablename__ = 'MenuItems'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    item_photo = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    weight = db.Column(db.Float)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('Subcategories.subcategory_id'))
    
    @property
    def photo_thumb(self):
        return Markup('<img height=\'50px\' src=\'/' + (self.item_photo if self.item_photo else '') + '\'>')
    
    @property
    def subcategory_name(self):
        subcategory_name = Subcategory.query.filter(Subcategory.subcategory_id == self.subcategory_id).first().subcategory_name
        return subcategory_name

def create_category(category_name):
    new_category = Category()
    new_category.category_name = category_name
    db.session.add(new_category)
    db.session.commit()
    return new_category

def create_menu_item(item_name, price, description, ingredients, weight, subcategory_id):
    new_item = MenuItem()
    new_item.item_name=item_name,
    new_item.price=price,
    new_item.description=description,
    new_item.ingredients=ingredients,
    new_item.weight=weight,
    new_item.subcategory_id=subcategory_id
    db.session.add(new_item)
    db.session.commit()
    return new_item

# Функция для получения всех позиций меню
def get_all_menu_items():
    return MenuItem.query.all()

# Функция для получения позиции меню по id
def get_menu_item_by_id(item_id):
    return MenuItem.query.get(item_id)

# Функция для обновления позиции меню
def update_menu_item(menu_item, new_data):
    menu_item.item_name = new_data["item_name"]
    menu_item.price = new_data["price"]
    menu_item.description = new_data["description"]
    menu_item.ingredients = new_data["ingredients"]
    menu_item.weight = new_data["weight"]
    menu_item.subcategory_id = new_data["subcategory_id"]
    db.session.commit()

# Функция для удаления позиции меню
def delete_menu_item(menu_item):
    db.session.delete(menu_item)
    db.session.commit()

# Функция для получения всех категорий
def get_all_categories():
    return Category.query.all()

# Функция для получения категории по id
def get_category_by_id(category_id):
    return Category.query.get(category_id)

# Функция для обновления категории
def update_category(category, new_category_name):
    category.category_name = new_category_name
    db.session.commit()

# Функция для удаления категории
def delete_category(category):
    db.session.delete(category)
    db.session.commit()
    
def create_subcategory(subcategory_name, category_id):
    new_subcategory = Subcategory()
    new_subcategory.subcategory_name = subcategory_name
    new_subcategory.category_id = category_id
    db.session.add(new_subcategory)
    db.session.commit()
    return new_subcategory

# Функция для получения всех подкатегорий
def get_all_subcategories():
    return Subcategory.query.all()

# Функция для получения подкатегории по id
def get_subcategory_by_id(subcategory_id):
    return Subcategory.query.get(subcategory_id)

# Функция для обновления подкатегории
def update_subcategory(subcategory, new_subcategory_name):
    subcategory.subcategory_name = new_subcategory_name
    db.session.commit()

# Функция для удаления подкатегории
def delete_subcategory(subcategory):
    db.session.delete(subcategory)
    db.session.commit()

# Функция для получения подкатегорий по id категории
def get_subcategories_by_category_id(category_id):
    return Subcategory.query.filter_by(category_id=category_id).all()

# Функция для получения позиций меню по id подкатегории
def get_menu_items_by_subcategory_id(subcategory_id):
    return MenuItem.query.filter_by(subcategory_id=subcategory_id).all()
