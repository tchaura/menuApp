-- Для таблицы MenuItems
ALTER TABLE MenuItems RENAME TO MenuItemsOld;  -- Переименование существующей таблицы
CREATE TABLE MenuItems (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    ingredients TEXT,
    weight REAL,
    item_photo TEXT,  -- Добавление нового столбца с новым именем
    subcategory_id INTEGER,
    FOREIGN KEY (subcategory_id) REFERENCES Subcategories (subcategory_id)
);
INSERT INTO MenuItems (item_id, item_name, price, description, ingredients, weight, item_photo, subcategory_id)
SELECT item_id, item_name, price, description, ingredients, weight, photo, subcategory_id
FROM MenuItemsOld;
DROP TABLE MenuItemsOld;  -- Удаление старой таблицы

-- Для таблицы Subcategories
ALTER TABLE Subcategories RENAME TO SubcategoriesOld;  -- Переименование существующей таблицы
CREATE TABLE Subcategories (
    subcategory_id INTEGER PRIMARY KEY,
    subcategory_name TEXT NOT NULL,
    category_id INTEGER,
    subcategory_photo TEXT,  -- Добавление нового столбца с новым именем
    FOREIGN KEY (category_id) REFERENCES Categories (category_id)
);
INSERT INTO Subcategories (subcategory_id, subcategory_name, category_id, subcategory_photo)
SELECT subcategory_id, subcategory_name, category_id, photo
FROM SubcategoriesOld;
DROP TABLE SubcategoriesOld;  -- Удаление старой таблицы
