from tornado.web import url

from apps.question.handler import *

urlpattern = (

    # 创建问答
    url('/questions/',QuestionHandler),

    url('/questions/([0-9]+)/',QuestionDetailHandler),

    # 问题回答
    url("/questions/([0-9]+)/answers/", AnswerHanlder),
    url("/answers/([0-9]+)/replys/", AnswerReplyHandler),
)