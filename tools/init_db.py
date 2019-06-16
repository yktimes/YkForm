from apps.users.models import User
from peewee import MySQLDatabase
from YkForm.settings import database
from apps.community.models import CommunityGroup,CommunityGroupMember,PostComment,Post,CommentLike
from apps.question.models import Question,Answer


def init():
    # database.create_tables([User])
    # database.create_tables([CommunityGroup,CommunityGroupMember])
    # database.create_tables([PostComment,Post,CommentLike])
    database.create_tables([Question,Answer])



if __name__ == '__main__':
    init()
