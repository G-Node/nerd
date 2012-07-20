from mongoengine import *

class Root(Document):
    # root fields
    author     = StringField()
    date       = StringField()
    repository = StringField()
    version    = StringField()

    # link to previous revison
    previous   = StringField()

    # collection of sections that belongs to root
    sections = ListField(StringField())