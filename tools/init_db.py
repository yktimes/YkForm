from apps.users.models import User
from peewee import MySQLDatabase
from YkForm.settings import database


def init():
    database.create_tables([User])


if __name__ == '__main__':
    init()
