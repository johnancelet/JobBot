from enum import Enum
from peewee import *

db = SqliteDatabase('job_database.db')

class BaseModel(Model):
    class Meta:
        database = db
    
    def upsert(self):
        self.insert()

class Person(BaseModel):
    link = CharField(primary_key=True)

    name = CharField(null=False)
    headline = CharField(null=False)
    company = CharField(null=False)
    location = CharField(null=False)

    visited = BooleanField(default=False)
    connection_state = IntegerField(null=False)

    # Can be parse later from headline
    position = CharField(null=True)

    def __str__(self):
        return 'Name: {0} Headline: {1} Visited: {2} Connection_State: {3}'\
            .format(self.name, self.headline, self.visited, self.connection_state)

    def __repr__(self):
        return '''
        Person(
            link="{0}",
            headline="{1}",
            company="{2}",
            location="{3}",
            visited={4},
            connection_state{5}
        )
        '''

class ConnectionState(Enum):
    Connected = 0
    CanConnect = 1
    CannotConnect = 2
    ConnectionPending = 3