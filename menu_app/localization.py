from .models import Translation
from . import db
from . import app
from wtforms import StringField
from copy import copy

LANGUAGES = copy(app.config['LANGUAGES'])
# primary lang to exclude from additional lang tabs
LANGUAGES.pop(app.config.get('DEFAULT_LANG'))


def after_model_change(self, form, model, is_created, localized_fields, model_name, id):
    for lang in LANGUAGES.keys():
        for field_name in localized_fields:
            translation_value = form[f'{field_name[0]}_{lang}'].data
            translation_attributes = {
                'language_code': lang,
                'reference_table': model_name,
                'reference_id': id,
                'reference_field': field_name[0],
                'translation_value': translation_value
            }

            if is_created:
                translation = Translation(**translation_attributes)
                db.session.add(translation)
            else:
                translation = Translation.query.filter_by(
                    language_code=lang,
                    reference_table=model_name,
                    reference_id=id,
                    reference_field=field_name[0]
                ).first()
                if translation:
                    translation.translation_value = translation_value
                else:
                    translation = Translation(**translation_attributes)
                    db.session.add(translation)
            db.session.commit()


def on_form_prefill(self, form, localized_fields, model_name, id):
    for lang in LANGUAGES.keys():
        for field_name in localized_fields:
            translation = Translation.query.filter_by(
                language_code=lang,
                reference_table=model_name,
                reference_id=id,
                reference_field=field_name[0]
            ).first()
            if translation:
                form[f'{field_name[0]}_{lang}'].data = translation.translation_value


def on_model_delete(self, model_name, localized_fields, id):
    for field_name in localized_fields:
        translations = Translation.query.filter_by(reference_table=model_name, reference_field=field_name[0],
                                                   reference_id=id).all()
        for translation in translations:
            db.session.delete(translation)

    db.session.commit()


def extra_fields_generator(localized_fields):
    extra_fields = {}
    for k, v in LANGUAGES.items():
        for field_name in localized_fields:
            if len(field_name) == 3:
                extra_fields.update(
                    {f'{field_name[0]}_{k}': field_name[2](label=f'{field_name[1]} ({v})', render_kw={'lang': v})})
            else:
                extra_fields.update(
                    {f'{field_name[0]}_{k}': StringField(label=f'{field_name[1]} ({v})', render_kw={'lang': v})})
    return extra_fields


def get_translated_model(reference_model, lang, id_row_name=None):
    translations = Translation.query.filter(Translation.language_code == lang,
                                            Translation.reference_table == reference_model.__tablename__)
    translated_model = []
    rows = db.session.query(reference_model).all()
    reference_fields = [column.key for column in reference_model.__table__.columns]

    for row in rows:
        id_row_name = id_row_name if id_row_name else f'{row.__class__.__name__.lower()}_id'
        row_id = getattr(row, id_row_name)
        modified_row = {id_row_name: row_id}
        for field in reference_fields:
            translation = translations.filter(Translation.reference_field == field,
                                              Translation.reference_id == row_id).first()
            translation_value = translation.translation_value if translation else ''
            modified_row[field] = translation_value if len(translation_value) > 0 else getattr(row, field)
        translated_model.append(modified_row)

    return translated_model


def get_translated_row(row_id, reference_model, lang, id_row_name=None):
    translated_model = get_translated_model(reference_model, lang, id_row_name)
    return list(filter(lambda row: row[id_row_name] == row_id, translated_model))[0]
