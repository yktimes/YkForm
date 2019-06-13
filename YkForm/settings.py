import peewee_async

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {


    "secret_key":'yksdm66hsbkjfbYY',
    "jwt_expire":30*24*3600,







    "MEDIA_ROOT": os.path.join(BASE_DIR,"media"),

    "SITE_URL":"http://127.0.0.1:8888",
    "redis":{

        "host":"127.0.0.1",
    }


}

database = peewee_async.MySQLDatabase(
    'ykforum',
    host='127.0.0.1',
    port=3306,
    user='root',
    password='mysql'
)