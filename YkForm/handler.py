from tornado.web import RequestHandler
import redis


class BaseHandler(RequestHandler):
    # 跨域
    def set_default_headers(self):
        # header('Access-Control-Allow-Origin:*'); // 允许所有来源访问
        # header('Access-Control-Allow-Method:POST,GET'); // 允许访问的方式 　　
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS POST, GET, DELETE, PUT, PATCH')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, tsessionid, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def options(self, *args, **kwargs):
        pass




class RedisHandler(BaseHandler):
    def __init__(self,application,request,**Kwargs):
        super().__init__(application,request,**Kwargs)

        self.redis_conn = redis.StrictRedis(**self.settings["redis"])

