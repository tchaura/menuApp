
from ast import Sub
from email.policy import default
from nis import cat
from flask_login import logout_user
from flask_sqlalchemy import SQLAlchemy
from markupsafe import Markup
db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'Categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    subcategories = db.relationship('Subcategory', backref='category', lazy=True)
    has_subcategories = db.Column(db.Integer, default = 0)
        

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
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'))
    
    @property
    def photo_thumb(self):
        return Markup('<img height=\'50px\' src=\'/' + (self.item_photo if self.item_photo else '') + '\'>')
    
    @property
    def subcategory_name(self):
        if (self.subcategory_id == 0):
            return ""
        
        subcategory_name = Subcategory.query.filter(Subcategory.subcategory_id == self.subcategory_id).first().subcategory_name
        return subcategory_name
    @property
    def category_name(self):
        if (self.category_id == 0):
            return ""
        
        category_name = Category.query.filter(Category.category_id == self.category_id).first().category_name
        return category_name

class Translation(db.Model):
    __tablename__ = "Translations"
    translation_id = db.Column(db.Integer, primary_key=True)
    language_code = db.Column(db.String(5), nullable=False)
    reference_table = db.Column(db.String(255), nullable=False)
    reference_id = db.Column(db.Integer, nullable=False)
    reference_field = db.Column(db.String(255), nullable=False)
    translation_value = db.Column(db.String(255), nullable=True)

    def __init__(self, language_code, reference_table, reference_id, reference_field, translation_value):
        self.language_code = language_code
        self.reference_table = reference_table
        self.reference_id = reference_id
        self.reference_field = reference_field
        self.translation_value = translation_value


class Information(db.Model):
    info_id = db.Column(db.Integer, primary_key = True)
    logo = db.Column(db.String(255), nullable = False)
    header_img = db.Column(db.String(255), nullable = False)
    title = db.Column(db.String(100), nullable = False)
    adress = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.String(100), nullable = False)
    wifi = db.Column(db.String(100), nullable = False)
    wifi_password = db.Column(db.String(100), nullable = False)
    
    @property
    def logo_thumb(self):
        return Markup('<img height=\'50px\' src=\'/' + (self.logo if self.logo else '') + '\'>')
    
    @property
    def header_thumb(self):
        return Markup('<img height=\'50px\' src=\'/' + (self.header_img if self.header_img else '') + '\'>')
