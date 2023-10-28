import os
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin.form.upload import FileUploadField
from wtforms import SelectField
from werkzeug.utils import secure_filename
from flask_babel import lazy_gettext as _
from . import db
from .login import MyAdminIndexView
import flask_login as login
from . import app
from .models import Category, Subcategory, MenuItem


# Views
class SubcategoryNameFilter(FilterEqual):
    def apply(self, query, value):
        return query.join(Subcategory).filter(Subcategory.subcategory_name == value)

    def operation(self):
        return 'равна'

class MenuItemModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    
    column_labels = dict(item_name= 'Имя', item_photo= 'Фото', subcategory_name = 'Подкатегория', photo_thumb = 'Фото')
    column_list = ('item_name', 'subcategory_name', 'photo_thumb')
    
    # Helper methods
    def get_subcategory_choices(self):
        subcategories = Subcategory.query.all()
        choices = [(s.subcategory_id, s.subcategory_name) for s in subcategories]
        return choices
    def get_subcategory_list(self):
        subcategories = Subcategory.query.all()
        choices = [(s.subcategory_name, s.subcategory_name) for s in subcategories]
        return choices
    
    # Filters config
    def get_filters(self):
        _dynamic_filters = getattr(self, 'dynamic_filters', None)
        if _dynamic_filters:
            return (super(MenuItemModelView, self).get_filters() or []) + _dynamic_filters
        else:
            return super(MenuItemModelView, self).get_filters()
    
    @expose('/')
    def index_view(self):
        self.dynamic_filters = [
            SubcategoryNameFilter(column=MenuItem.subcategory_name, name='Подкатегория', options=self.get_subcategory_list) 
        ]
        self._refresh_filters_cache()
        return super(MenuItemModelView, self).index_view()
    

    # Forms config
    form_overrides = {
        'item_photo': FileUploadField,
    }
    form_args = {
        'item_photo': {
            'label': 'Фото блюда',
            'base_path': 'menu_app/static/img/menu_items',
            'namegen': None 
        },
    }
    form_extra_fields = {
        'subcategory_id': SelectField(
            label='Подкатегория',
        )
    }
    def create_form(self):
        form = super().create_form()
        form.subcategory_id.choices = self.get_subcategory_choices()
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        form.subcategory_id.choices = self.get_subcategory_choices()
        return form
    
    def on_model_change(self, form, model, is_created):
        if form.item_photo.data:
            # if photo is not changed, do nothing
            if form.item_photo.data == model.item_photo:
                return
            
            filename = secure_filename(form.item_photo.data.filename)
            # form.subcategory_photo.data.save(os.path.join(app.root_path, f'static/img/subcategories/', filename))
            
            model.item_photo = 'static/img/menu_items/' + filename
            
            if not is_created and form.item_photo.object_data:
                old_filename = form.item_photo.object_data
                if os.path.exists(os.path.join(app.root_path, old_filename)):
                    os.remove(os.path.join(app.root_path, old_filename))
    
class CategoryModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    
# Filter for Subcategories
class CategoryNameFilter(FilterEqual):
    def apply(self, query, value):
        return query.join(Category).filter(Category.category_name == value)

    def operation(self):
        return 'равна'
    
class SubcategoryModelView(ModelView):
    
    def is_accessible(self):
        return login.current_user.is_authenticated    
    
    column_labels = dict(subcategory_name= 'Имя', subcategory_photo= 'Фото', category_name = 'Категория', photo_thumb = 'Фото')
    column_list = ('subcategory_name', 'category_name', 'photo_thumb')
    
    # Helper methods
    def get_category_choices(self):
        categories = Category.query.all()
        choices = [(c.category_id, c.category_name) for c in categories]
        return choices
    def get_category_list(self):
        categories = Category.query.all()
        choices = [(c.category_name, c.category_name) for c in categories]
        return choices
    
    # Filters config
    def get_filters(self):
        _dynamic_filters = getattr(self, 'dynamic_filters', None)
        if _dynamic_filters:
            return (super(SubcategoryModelView, self).get_filters() or []) + _dynamic_filters
        else:
            return super(SubcategoryModelView, self).get_filters()
    
    @expose('/')
    def index_view(self):
        self.dynamic_filters = [
            CategoryNameFilter(column=Subcategory.category_name, name='Категория', options=self.get_category_list) 
        ]
        self._refresh_filters_cache()
        return super(SubcategoryModelView, self).index_view()
    

    # Forms config
    form_overrides = {
        'subcategory_photo': FileUploadField,
    }
    form_args = {
        'subcategory_photo': {
            'label': 'Фото подкатегории',
            'base_path': 'menu_app/static/img/subcategories',
            'namegen': None 
        },
    }
    form_extra_fields = {
        'category_id': SelectField(
            label='Категории',
        )
    }
    def create_form(self):
        form = super().create_form()
        form.category_id.choices = self.get_category_choices()
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        form.category_id.choices = self.get_category_choices()
        return form
    
    def on_model_change(self, form, model, is_created):
        if form.subcategory_photo.data:
            # if photo is not changed, do nothing
            if form.subcategory_photo.data == model.subcategory_photo:
                return
            
            filename = secure_filename(form.subcategory_photo.data.filename)
            # form.subcategory_photo.data.save(os.path.join(app.root_path, f'static/img/subcategories/', filename))
            
            model.subcategory_photo = 'static/img/subcategories/' + filename
            
            if not is_created and form.subcategory_photo.object_data:
                old_filename = form.subcategory_photo.object_data
                if os.path.exists(os.path.join(app.root_path, old_filename)):
                    os.remove(os.path.join(app.root_path, old_filename))
                

admin = Admin(app, name='Панель администратора', template_mode='bootstrap4', index_view=MyAdminIndexView(), base_template='my_master.html', translations_path='./translations')
admin.add_view(CategoryModelView(Category, db.session, name='Категории'))
admin.add_view(SubcategoryModelView(Subcategory, db.session, name='Подкатегории'))
admin.add_view(MenuItemModelView(MenuItem, db.session, name="Блюда"))

