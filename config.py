import configparser
from datetime import timedelta

cfg = configparser.ConfigParser()
cfg.read("config.cfg")

class config:
    SQLALCHEMY_DATABASE_URI = "%s+%s://%s:%s@%s:%s/%s" % (
        cfg["database"]["default_connection"],
        cfg["mysql"]["driver"],
        cfg["mysql"]["user"],
        cfg["mysql"]["password"],
        cfg["mysql"]["host"],
        cfg["mysql"]["port"],
        cfg["mysql"]["db"],
    )
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_SECRET_KEY = cfg["jwt"]["secret_key"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    UPLOAD_MEDIA_AVATAR = "/storage/media/avatar"
    UPLOAD_MEDIA_VIDEO = "/storage/media/video"
    UPLOAD_MEDIA_PRESENTATION = "/storage/media/presentation"
    ACCESS_KEY_ID = cfg["aws"]["key_id"]
    ACCESS_SECRET_KEY = cfg["aws"]["secret_key"]
    BUCKET_NAME = cfg["aws"]["bucket"]

class DevelopmentConfig(config):
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000

class ProductionConfig(config):
    APP_DEBUG = False
    DEBUG = False
    MAX_BYTES = 10000

<<<<<<< HEAD
class Testing:
=======
class TestingConfig(config):
>>>>>>> 88ad2993b973a9ca66d40ffcbcd2e24386e6a47d
    APP_DEBUG = True
    DEBUG = True
    MAX_BYTES = 10000
    SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s_testing' % (
        cfg['database']['default_connection'],
        cfg['mysql']['driver'],
        cfg['mysql']['user'],
        cfg['mysql']['password'],
        cfg['mysql']['host'],
        cfg['mysql']['port'],
        cfg['mysql']['db'],
    )
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_SECRET_KEY = cfg['jwt']['secret_key']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    ACCESS_KEY_ID = cfg["aws"]["key_id"]
    ACCESS_SECRET_KEY = cfg["aws"]["secret_key"]
    BUCKET_NAME = cfg["aws"]["bucket"]