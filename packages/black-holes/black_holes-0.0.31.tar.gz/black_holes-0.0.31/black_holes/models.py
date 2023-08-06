import datetime
from peewee import *

db = SqliteDatabase('black_holes.db')


class BaseModel(Model):
    class Meta:
        database = db


class Secret(BaseModel):
    created_date = DateTimeField(default=datetime.datetime.now)
    key = CharField(unique=True, primary_key=True)
    value = BareField()

