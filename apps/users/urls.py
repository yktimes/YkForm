from tornado.web import url
from apps.users.handler import SmsHandler,RegesterHandler


urlpattern = (

    url('/code/',SmsHandler),
    url('/register/',RegesterHandler),
)