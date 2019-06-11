from tornado.web import url
from apps.users.handler import SmsHandler,RegesterHandler,LoginHandler


urlpattern = (

    url('/code/',SmsHandler),
    url('/register/',RegesterHandler),
    url('/login/',LoginHandler),
)