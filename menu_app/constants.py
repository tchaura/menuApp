import os

STATIC_PATH = '/static'
MAIN_SITE_URL = None
APP_ROOT_FOLDER_PATH = os.path.dirname(__file__).split("/")[-1] + "/" # should be menu_app/

MAIN_SITE_LOCALE_PATHS = {
    'en': '',
    'ge': 'ka',
    'tr': 'tr',
    'he': 'he',
    'ru': 'ru'
}