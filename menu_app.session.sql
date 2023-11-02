CREATE TABLE MenuItems_New (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT,
    ingredients TEXT,
    weight REAL,
    item_photo TEXT,
    category_id INTEGER,
    subcategory_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES Categories (category_id),
    FOREIGN KEY (subcategory_id) REFERENCES Subcategories (subcategory_id)
);

DROP TABLE MenuItems;
ALTER TABLE MenuItems_New RENAME TO MenuItems;
