import os
POSTGRES_USER = os.environ['USER_FOR_DOCKER']
POSTGRES_PASSWORD = os.environ['PASSWORD_FOR_DOCKER']
class Settings_app():
    def __init__(self):
        self.domenServer = 'http://127.0.0.1:5000/'
        self.app_db_connect = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/db_docker'
