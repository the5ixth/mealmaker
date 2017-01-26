import os

class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:lornad@localhost:3306/meal'

    SECRET_KEY = 'key'

    UPLOAD_FOLDER = '/home/the5ixth/Desktop/meal/mealmaker/app/static/meals'


class ProdConfig(DevConfig):
    SECRET_KEY = os.environ.get("FLASK_SECRET") or "dev_key"
    UPLOAD_FOLDER = "/opt/python/current/app/app/static/meals"
    if os.environ.get("RDS_HOSTNAME"):
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + \
                                  os.environ["RDS_USERNAME"] + ":" + \
                                  os.environ["RDS_PASSWORD"] + "@" + \
                                  os.environ["RDS_HOSTNAME"] + ":" + \
                                  os.environ["RDS_PORT"] + "/" + \
                                  os.environ["RDS_DB_NAME"]


config_types = {'dev': DevConfig,
                'prod': ProdConfig}