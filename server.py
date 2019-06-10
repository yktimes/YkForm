from tornado import web
from YkForm.urls import urlpattern
from YkForm.settings import settings
import tornado
import peewee_async
from YkForm.settings import database

if __name__ == '__main__':
    # 集成json到wtforms
    import wtforms_json

    wtforms_json.init()

    app = web.Application(
        urlpattern, debug=True, **settings
    )
    app.listen(8888)

    # 全局设置 Manager
    objects = peewee_async.Manager(database)

    database.set_allow_sync(False)

    app.objects = objects


    tornado.ioloop.IOLoop.current().start()