from peewee import *

db = SqliteDatabase('job_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Person(BaseModel):
    relative_link = CharField(primary_key=True)
    full_link = CharField()
    name = CharField()
    title = CharField()
    position = CharField(null=True)
    company = CharField(null=True)
    location = CharField(null=True)

    visited = BooleanField(default=False)
    connected = BooleanField(default=False)