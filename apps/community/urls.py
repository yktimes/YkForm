from tornado.web import url

from apps.community.handler import GroupHandler,GroupMemberHandler,GroupDetailHandler

urlpattern = (

    url('/groups/',GroupHandler),
    url('/groups/([0-9]+)/members/',GroupMemberHandler),
    # 获取小组信息
    url('/groups/([0-9]+)/',GroupDetailHandler),

)