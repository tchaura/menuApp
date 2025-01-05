import os

from flask_sqlalchemy import SQLAlchemy
from .models import Subcategory, MenuItem

def rename_static_files(db: SQLAlchemy):
    for entity_name, entity_meta in ENTITIES_TO_RENAME.items():
        entity_class = globals()[entity_name]
        photo_field = entity_meta['photo']

        entities = entity_class.query.filter(getattr(entity_class, photo_field) != "")
        renamed_files = set()
        for entity in entities:
            _rename_file(entity, entity_class, entity_meta, renamed_files, db)

def _rename_file(entity, entity_class, entity_meta, renamed_files, db):
    cur_path = getattr(entity, entity_meta['photo'])

    if cur_path is None:
        return
    if not os.path.exists('menu_app/' + cur_path):
        setattr(entity, entity_meta['photo'], "")
        return

    file_extension = os.path.splitext(cur_path)[1]
    target_path = os.path.join(f"static/img/{entity_meta['dir_prefix']}/", str(getattr(entity, entity_meta['id'])) + file_extension)

    if cur_path == target_path:
        renamed_files.add(target_path)
        return

    if cur_path in renamed_files:
        setattr(entity, entity_meta['photo'], "")
        return

    if os.path.exists('menu_app/' + target_path):
        while db.session.query(entity_class.query.filter(
            getattr(entity_class, entity_meta['photo']) == target_path
        ).exists()).scalar():
            conflicting_entity = entity_class.query.filter(
                getattr(entity_class, entity_meta['photo']) == target_path
            ).first()
            _rename_file(conflicting_entity, entity_class, entity_meta, renamed_files, db)

    os.rename('menu_app/' + cur_path, 'menu_app/' + target_path)
    setattr(entity, entity_meta['photo'], target_path)
    db.session.commit()

    renamed_files.add(target_path)

ENTITIES_TO_RENAME = {
    'MenuItem': {
        'dir_prefix': 'menu_items',
        'id': 'item_id',
        'photo': 'item_photo'
    },
    'Subcategory': {
        'dir_prefix': 'subcategories',
        'id': 'subcategory_id',
        'photo': 'subcategory_photo'
    },
}
