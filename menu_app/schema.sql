create table Categories
(
    category_id       INTEGER not null
        primary key,
    category_name     VARCHAR not null,
    has_subcategories INTEGER
);

create table Subcategories
(
    subcategory_id    INTEGER not null
        primary key,
    subcategory_name  VARCHAR not null,
    subcategory_photo TEXT    not null,
    category_id       INTEGER
        references Categories
);

create table MenuItems
(
    item_id        INTEGER not null
        primary key,
    item_name      VARCHAR not null,
    item_photo     TEXT,
    price          FLOAT   not null,
    description    TEXT,
    ingredients    TEXT,
    weight         text,
    subcategory_id INTEGER
        references Subcategories,
    category_id    INTEGER
        references Categories,
    measure_unit   varchar(10) default 'g'
);

create table Translations
(
    translation_id    INTEGER      not null
        primary key,
    language_code     VARCHAR(5)   not null,
    reference_table   VARCHAR(255) not null,
    reference_id      INTEGER      not null,
    reference_field   VARCHAR(255) not null,
    translation_value VARCHAR(255)
);

create table information
(
    info_id       INTEGER      not null
        primary key,
    logo          VARCHAR(255) not null,
    header_img    VARCHAR(255) not null,
    title         VARCHAR(100) not null,
    adress        VARCHAR(100) not null,
    phone         VARCHAR(100) not null,
    wifi          VARCHAR(100) not null,
    wifi_password VARCHAR(100)
);

create table popup
(
    popup_id         INTEGER not null
        primary key,
    popup_img        VARCHAR(255),
    show_always      BOOLEAN,
    show             BOOLEAN,
    background_click BOOLEAN,
    close_timeout    INTEGER
);

create table user
(
    id       INTEGER not null
        primary key,
    login    VARCHAR(80)
        unique,
    password VARCHAR(64)
);

