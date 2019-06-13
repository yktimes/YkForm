from apps.users.models import User
from peewee import MySQLDatabase
from YkForm.settings import database
from apps.community.models import CommunityGroup,CommunityGroupMember

def init():
    # database.create_tables([User])
    database.create_tables([CommunityGroup,CommunityGroupMember])



if __name__ == '__main__':
    init()
