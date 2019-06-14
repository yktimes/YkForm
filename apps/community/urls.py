from tornado.web import url

from apps.community.handler import *

urlpattern = (

    # 创建小组
    url('/groups/',GroupHandler),
    # 申请加入小组
    url('/groups/([0-9]+)/members/',GroupMemberHandler),
    # 获取小组信息
    url('/groups/([0-9]+)/',GroupDetailHandler),

    # 新建帖子
    url('/groups/([0-9]+)/posts/',PostHandler),
    # 帖子详情
    url('/posts/([0-9]+)/',PostDetailHandler),

)