import secrets
import string
from datetime import timedelta

def generate_alphanum_crypt_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(secrets.choice(
        letters_and_digits) for i in range(length))


def __set_config_ap(APP, Settings_app):
    APP.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
    APP.config['LST_CREATE_DIRRECTORY'] = []
    # !!!!!--- Индексы не менять!!!! -------!!!!!!!!!!

    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    APP.permanent_session_lifetime = timedelta(days=1)

    APP.config['SECRET_KEY_API'] = '0b606c7dc8323ac2f6e64efce5d65c465206a1ae8a8f14cb23'
    APP.config['SQLALCHEMY_DATABASE_URI'] = Settings_app.app_db_connect
    return APP

