from mongoengine import *
from elements.property import Property

# Section is first order document
class Section(Document):
    # id, implemented as hash of its content
    sid = StringField()

    # section fields
    name       = StringField()
    type_name  = StringField()
    reference  = StringField() # id, primary key, indification
    definition = StringField()
    repository = StringField()
    mapping    = StringField() # URL
    # TODO: implement method for parsing path to section
    # or put just a path
    link       = ReferenceField(Section)
    include    = StringField() # URL