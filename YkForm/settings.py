import peewee_async

settings = {

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