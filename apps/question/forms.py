from wtforms_tornado import Form
from wtforms import StringField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Regexp,AnyOf,Length




class QuestionForm(Form):
    title = StringField("名称",validators=[DataRequired("请输入标题")])
    category = StringField("类别",validators=[AnyOf(values=["技术问答", "技术分享","活动建议"])])
    content = StringField("内容", validators=[DataRequired(message="请输入内容")])

class AnswerForm(Form):
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=3, message="内容不能少于3个字符")])

class AnswerReplyForm(Form):
    replyed_user = IntegerField("回复用户", validators=[DataRequired("请输入回复用户")])
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=3, message="内容不能少于3个字符")])


