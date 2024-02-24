import os

import flask_login as login
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin.form.upload import FileUploadField, ImageUploadField
from werkzeug.utils import secure_filename
from wtforms import SelectField, BooleanField, TextAreaField

from . import app
from . import db
from . import localization
from .localization import extra_fields_generator
from .login import MyAdminIndexView
from .models import Category, Information, Subcategory, MenuItem
from .pillow import compress


class SubcategoryNameFilter(FilterEqual):
    def apply(self, query, value):
        return query.join(Subcategory).filter(Subcategory.subcategory_name == value)

    def operation(self):
        return 'равна'


class CategoryNameFilter(FilterEqual):
    def apply(self, query, value):
        return query.join(Category).filter(Category.category_name == value)

    def operation(self):
        return 'равна'


class MenuItemModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    create_template = 'admin/menu_item_form_create.html'
    edit_template = 'admin/menu_item_form_edit.html'

    # Остальные настройки представления

    column_labels = dict(item_name='Название блюда', item_photo='Фото', subcategory_name='Подкатегория',
                         photo_thumb='Фото',
                         ingredients='Состав', description='Описание', price='Цена (разделяется запятой)', weight='Вес',
                         category_name='Категория', measure_unit='Единица измерения')
    column_list = ('item_name', 'subcategory_name', 'category_name', 'photo_thumb', 'measure_unit')

    # Helper methods
    def get_subcategory_choices(self):
        subcategories = Subcategory.query.all()
        subcategory_choices = [(s.subcategory_id, s.subcategory_name) for s in subcategories]
        # subcategory_choices.append((0, 'Без категории'))
        return subcategory_choices

    def get_subcategory_list(self):
        subcategories = Subcategory.query.all()
        choices = [(s.subcategory_name, s.subcategory_name) for s in subcategories]
        # choices.append((0, 'Без категории'))
        return choices

    def get_category_choices(self):
        categories = Category.query.filter(Category.has_subcategories == 0)
        category_choices = [(c.category_id, c.category_name) for c in categories]
        # category_choices.append((0, 'Без категории'))
        return category_choices

    def get_category_list(self):
        categories = Category.query.filter(Category.has_subcategories == 0)
        category_choices = [(c.category_name, c.category_name) for c in categories]
        #    category_choices.append((0, 'Без категории'))
        return category_choices

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
            SubcategoryNameFilter(column=MenuItem.subcategory_name, name='Подкатегория',
                                  options=self.get_subcategory_list),
            CategoryNameFilter(column=MenuItem.category_name, name='Категория', options=self.get_category_list)
        ]
        self._refresh_filters_cache()
        return super(MenuItemModelView, self).index_view()

    form_overrides = {
        'item_photo': ImageUploadField,
        'measure_unit': SelectField,
    }
    form_args = {
        'item_photo': {
            'label': 'Фото блюда (без русских символов в названии)',
            'base_path': 'menu_app/static/img/menu_items',
            'namegen': lambda obj, file_data: "temp" + os.path.splitext(file_data.filename)[1]
        },
        'measure_unit': {
            'label': 'Единица измерения',
            'choices': [('g', 'граммы'), ('ml', 'миллилитры')],
            'default': 'g'
        }
    }

    form_extra_fields = {
        'bindToSubcategory': BooleanField(
            label='Привязать к подкатегории'
        ),
        'bindToCategory': BooleanField(
            label='Привязать к категории'
        ),
        'subcategory_id': SelectField(
            label='Подкатегория',
            validate_choice=False
        ),
        'category_id': SelectField(
            label='Категория',
            validate_choice=False
        )
    }

    localized_fields = [('item_name', 'Название блюда'), ('description', 'Описание', TextAreaField),
                        ('ingredients', 'Состав', TextAreaField)]
    form_extra_fields.update(extra_fields_generator(localized_fields))

    def after_model_change(self, form, model, is_created, localized_fields=localized_fields):
        localization.after_model_change(self, form, model, is_created, localized_fields, 'MenuItems', model.item_id)

    def on_form_prefill(self, form, id, localized_fields=localized_fields):
        localization.on_form_prefill(self, form, localized_fields, 'MenuItems', id)

    def on_model_delete(self, model, localized_fields=localized_fields):
        localization.on_model_delete(self, 'MenuItems', localized_fields, model.item_id)

    def create_form(self, **kwargs):
        form = super().create_form()
        form.subcategory_id.choices = self.get_subcategory_choices()
        form.category_id.choices = self.get_category_choices()
        return form

    def edit_form(self, obj):
        form = super().edit_form(obj)
        form.subcategory_id.choices = self.get_subcategory_choices()
        form.category_id.choices = self.get_category_choices()
        if obj.category_id == 0:
            form.bindToCategory.render_kw = {'default': 'false'}
        else:
            form.bindToCategory.render_kw = {'default': 'true'}
        return form

    def on_model_change(self, form, model, is_created):
        if form.bindToCategory.data is True:
            model.category_id = form.category_id.data
            model.subcategory_id = 0
        else:
            model.subcategory_id = form.subcategory_id.data
            model.category_id = 0

        if form.item_photo.data:

            # if photo is not changed, do nothing
            if form.item_photo.data == model.item_photo:
                return

            temp_path = os.path.join('menu_app/static/img/menu_items', secure_filename(form.item_photo.data.filename))
            file_extension = os.path.splitext(temp_path)[1]
            compress(temp_path)
            # form.subcategory_photo.data.save(os.path.join(app.root_path, f'static/img/subcategories/', filename))
            os.rename(temp_path, os.path.join('menu_app/static/img/menu_items', str(model.item_id) + file_extension))

            model.item_photo = 'static/img/menu_items/' + str(model.item_id) + file_extension
            if not is_created and form.item_photo.object_data:
                old_filename = form.item_photo.object_data
                if old_filename == model.item_photo:
                    return
                if os.path.exists(os.path.join(app.root_path, old_filename)):
                    os.remove(os.path.join(app.root_path, old_filename))


class CategoryModelView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_labels = dict(category_name='Имя категории', has_subcategories='Добавление подкатегорий')
    column_formatters = {
        'has_subcategories': lambda v, c, m, p: 'Да' if m.has_subcategories else 'Нет'
    }

    form_extra_fields = {
        'has_subcategories': SelectField('Добавление подкатегории', choices=[(1, 'Да'), (0, 'Нет')], coerce=int)
    }

    localized_fields = [('category_name', 'Имя категории')]
    form_extra_fields.update(extra_fields_generator(localized_fields))

    def after_model_change(self, form, model, is_created, localized_fields=localized_fields):
        localization.after_model_change(self, form, model, is_created, localized_fields, 'Categories',
                                        model.category_id)

    def on_form_prefill(self, form, id, localized_fields=localized_fields):
        localization.on_form_prefill(self, form, localized_fields, 'Categories', id)

    def on_model_delete(self, model, localized_fields=localized_fields):
        localization.on_model_delete(self, 'Categories', localized_fields, model.category_id)


class SubcategoryModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

    create_template = 'admin/subcategory_form.html'
    edit_template = 'admin/subcategory_form.html'

    column_labels = dict(subcategory_name='Имя', category_name='Категория', photo_thumb='Фото')
    column_list = ('subcategory_name', 'category_name', 'photo_thumb')

    # Helper methods
    def get_category_choices(self):
        categories = Category.query.filter(Category.has_subcategories == 1)
        choices = [(c.category_id, c.category_name) for c in categories]
        return choices

    def get_category_list(self):
        categories = Category.query.filter(Category.has_subcategories == 1)
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
        'subcategory_photo': ImageUploadField,
    }
    form_args = {
        'subcategory_photo': {
            'label': 'Фото подкатегории (без русских символов в названии)',
            'base_path': 'menu_app/static/img/subcategories',
            'namegen': lambda obj, file_data: "temp" + os.path.splitext(file_data.filename)[1]
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

    localized_fields = [('subcategory_name', 'Имя подкатегории')]
    form_extra_fields.update(extra_fields_generator(localized_fields))

    def after_model_change(self, form, model, is_created, localized_fields=localized_fields):
        localization.after_model_change(self, form, model, is_created, localized_fields, 'Subcategories',
                                        model.subcategory_id)

    def on_form_prefill(self, form, id, localized_fields=localized_fields):
        localization.on_form_prefill(self, form, localized_fields, 'Subcategories', id)

    def on_model_delete(self, model, localized_fields=localized_fields):
        localization.on_model_delete(self, 'Subcategories', localized_fields, model.subcategory_id)

    def on_model_change(self, form, model, is_created):
        if form.subcategory_photo.data:
            # if photo is not changed, do nothing
            if form.subcategory_photo.data == model.subcategory_photo:
                return

            temp_path = os.path.join('menu_app/static/img/subcategories', secure_filename(form.subcategory_photo.data.filename))
            file_extension = os.path.splitext(temp_path)[1]
            compress(temp_path)
            os.rename(temp_path, os.path.join('menu_app/static/img/subcategories', str(model.subcategory_id) + file_extension))

            model.item_photo = 'static/img/subcategories' + str(model.subcategory_id) + file_extension

            if not is_created and form.subcategory_photo.object_data:
                old_filename = form.subcategory_photo.object_data
                if old_filename == model.subcategory_photo:
                    return
                if os.path.exists(os.path.join(app.root_path, old_filename)):
                    os.remove(os.path.join(app.root_path, old_filename))


class InformationView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    form_extra_fields = {}

    create_template = 'admin/information_form.html'
    edit_template = 'admin/information_form.html'

    localized_fields = [('title', 'Заголовок'), ('adress', 'Адрес'), ]
    form_extra_fields.update(extra_fields_generator(localized_fields))

    def after_model_change(self, form, model, is_created, localized_fields=localized_fields):
        localization.after_model_change(self, form, model, is_created, localized_fields, 'information', model.info_id)

    def on_form_prefill(self, form, id, localized_fields=localized_fields):
        localization.on_form_prefill(self, form, localized_fields, 'information', id)

    def on_model_delete(self, model, localized_fields=localized_fields):
        localization.on_model_delete(self, 'information', localized_fields, model.info_id)

    column_labels = dict(title='Заголовок', adress='Адрес', phone='Телефон', wifi='WiFi', wifi_password='Пароль WiFi',
                         logo_thumb='Логотип (без русских символов в названии)',
                         header_thumb='Шапка (без русских символов в названии)')
    column_list = ('title', 'adress', 'phone', 'wifi', 'wifi_password', 'logo_thumb', 'header_thumb')

    form_overrides = {
        'logo': ImageUploadField,
        'header_img': ImageUploadField,
    }
    form_args = {
        'logo': {
            'label': 'Логотип сайта',
            'base_path': 'menu_app/static/img/info',
            'namegen': None
        },
        'header_img': {
            'label': 'Шапка',
            'base_path': 'menu_app/static/img/info',
            'namegen': None
        },
    }

    def on_model_change(self, form, model, is_created):
        for field in ['logo', 'header_img']:
            if form[field].data:
                # if photo is not changed, do nothing
                if field == 'logo':
                    if form[field].data == model.logo:
                        continue
                else:
                    if form[field].data == model.header_img:
                        continue

                filename = secure_filename(form[field].data.filename)
                compress(os.path.join('menu_app/static/img/info', form[field].data.filename))

                if field == 'logo':
                    model.logo = 'static/img/info/' + filename
                else:
                    model.header_img = 'static/img/info/' + filename

                if not is_created and form[field].object_data:
                    old_filename = form[field].object_data
                    if field == 'logo':
                        if old_filename == model.logo:
                            return
                    else:
                        if old_filename == model.header_img:
                            return
                    if os.path.exists(os.path.join(app.root_path, old_filename)):
                        os.remove(os.path.join(app.root_path, old_filename))


admin = Admin(app, name='Панель администратора', template_mode='bootstrap4', index_view=MyAdminIndexView(),
              base_template='my_master.html', translations_path='./translations')
admin.add_view(InformationView(Information, db.session, name="Информация"))
admin.add_view(CategoryModelView(Category, db.session, name='Категории'))
admin.add_view(SubcategoryModelView(Subcategory, db.session, name='Подкатегории'))
admin.add_view(MenuItemModelView(MenuItem, db.session, name="Блюда"))
