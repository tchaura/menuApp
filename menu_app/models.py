from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создайте объект для подключения к базе данных
engine = create_engine('sqlite:///menu_app/db.sqlite')
# Создайте базовый класс для определения модели
Base = declarative_base()

# Определите модели данных для таблиц Subcategories и MenuItems
class Category(Base):
    __tablename__ = 'Categories'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    
class Subcategory(Base):
    __tablename__ = 'Subcategories'
    subcategory_id = Column(Integer, primary_key=True)
    subcategory_name = Column(String, nullable=False)
    category_id = Column(Integer)
    subcategory_photo = Column(Text)

class MenuItem(Base):
    __tablename__ = 'MenuItems'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text)
    ingredients = Column(Text)
    weight = Column(Float)
    item_photo = Column(Text)
    subcategory_id = Column(Integer, ForeignKey('Subcategories.subcategory_id'))

# Создайте сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()



# Теперь вы можете использовать модели Subcategory и MenuItem для выполнения запросов к базе данных.
def add_category(category_name):
    new_category = Category(category_name=category_name)
    session.add(new_category)
    session.commit()

# Функция для получения всех категорий
def get_all_categories():
    return session.query(Category).all()

# Функция для добавления новой подкатегории
def add_subcategory(subcategory_name, category_id, subcategory_photo=None):
    new_subcategory = Subcategory(subcategory_name=subcategory_name, category_id=category_id, subcategory_photo=subcategory_photo)
    session.add(new_subcategory)
    session.commit()

# Функция для получения всех подкатегорий
def get_all_subcategories():
    return session.query(Subcategory).all()

# Функция для добавления новой позиции меню
def add_menu_item(item_name, price, description, ingredients, weight, subcategory_id, item_photo = None):
    new_item = MenuItem(
        item_name=item_name,
        price=price,
        description=description,
        ingredients=ingredients,
        weight=weight,
        item_photo=item_photo,
        subcategory_id=subcategory_id
    )
    session.add(new_item)
    session.commit()

# Функция для получения всех позиций меню
def get_all_menu_items():
    return session.query(MenuItem).all()

# Функция для получения подкатегорий по id категории
def get_subcategories_by_category_id(category_id):
    return session.query(Subcategory).filter(Subcategory.category_id == category_id).all()

# Функция для получения позиций меню по id подкатегории
def get_menu_items_by_subcategory_id(subcategory_id):
    return session.query(MenuItem).filter(MenuItem.subcategory_id == subcategory_id).all()
