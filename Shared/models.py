from typing import Optional

from peewee import *

from Shared.constants import Const

db = SqliteDatabase("job_database.db")


class ModelConstants(Const):
    class DELIMITER(Const):
        TOKEN = ","
        ANSWER = "\n"


class CustomBaseModel(Model):
    class Meta:
        database = db


class Job(CustomBaseModel):
    # Job fields
    key = CharField()
    website = CharField()
    link = TextField()
    title = CharField()
    description = TextField(null=True)
    company = TextField(null=True)
    city = CharField(null=True)
    state = CharField(null=True)  # TODO: Rename this to region
    country = CharField(null=True)
    posted_date = DateField(null=True)
    expired = BooleanField(default=False)
    location = CharField(null=True)

    # Application fields
    easy_apply = BooleanField(default=False)
    applied = BooleanField(default=False)
    attempted = BooleanField(default=False)
    access_date = DateField(null=True)
    error = TextField(null=True)
    message = TextField(null=True)
    good_fit = BooleanField(default=True)

    class Meta:
        primary_key = CompositeKey("key", "website")


"""
These next two models are for the application builder
"""


class Blurb(CustomBaseModel):
    id = PrimaryKeyField()
    long_text = TextField(null=False)
    short_text = TextField(null=False)
    score = IntegerField(default=1)

    @staticmethod
    def get_header():
        return "Blurb Header\nid :: Blurb\n\n"

    def __str__(self):
        return "{0} :: {1}".format(self.id, self.short_text)


class Tag(CustomBaseModel):
    id = PrimaryKeyField()
    text = CharField(null=False)
    blurb = ForeignKeyField(Blurb, related_name="tags")
    type = CharField(null=True)  # Example mechanical or software?

    @staticmethod
    def get_header():
        return "Tag Header\nid :: blurbId :: text\n\n"

    def __str__(self):
        return "{0} :: {1} :: {2}".format(self.id, self.blurb.id, self.text)


# These class are for LinkedIn


class Person(CustomBaseModel):
    relative_link = CharField(primary_key=True)
    full_link = CharField()
    name = CharField()
    title = CharField()
    position = CharField(null=True)
    company = CharField(null=True)
    location = CharField(null=True)

    visited = BooleanField(default=False)
    connected = BooleanField(default=False)
