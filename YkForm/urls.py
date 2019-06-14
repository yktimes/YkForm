from apps.users import urls as user_urls
from apps.community import urls as community_urls

from tornado.web import url
from tornado.web import StaticFileHandler
from YkForm.settings import settings
from apps.ueditor import urls as ueditor_urls
urlpattern = [


    (url('/media/(.*)',StaticFileHandler,{'path':settings["MEDIA_ROOT"]}))

]

urlpattern+=user_urls.urlpattern
urlpattern+=community_urls.urlpattern
urlpattern+=ueditor_urls.urlpattern