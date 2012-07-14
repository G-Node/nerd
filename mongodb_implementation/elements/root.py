from mongoengine import *
from elements.section import Section

class Root(Document):
    # TODO:
    # there should be some kind of uniq indificator

    # root fields
    author     = StringField()
    date       = StringField()
    repository = StringField()
    version    = StringField()

    # collection of sections that belongs to root
    sections = ListField(EmbeddedDocumentField(Section))
