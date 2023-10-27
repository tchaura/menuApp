from os import name
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import lazy_gettext as _
from flask_babel import Babel
from . import babel
from . import db
from .login import MyAdminIndexView, MyModelView, User
import flask_login as login
from . import app
from .models import Category, Subcategory, MenuItem

# Создайте объект Flask-Admin
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4', index_view=MyAdminIndexView(), base_template='my_master.html')

class MenuItemModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    
class CategoryModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    
class SubcategoryModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    
    
admin.add_view(CategoryModelView(Category, db.session, name='Категории'))
admin.translations_path = './translations'
admin.name = _('Администратор')
admin.add_view(SubcategoryModelView(Subcategory, db.session, name='Подкатегории'))
admin.add_view(MenuItemModelView(MenuItem, db.session, name="Блюда"))
# admin.add_view(MyModelView(User, db.session))

