from mongoengine import *
import hashlib

from elements.property import Property

# Section is first order document
class Section(EmbeddedDocument):

    # section fields
    name       = StringField()
    type_name  = StringField()
    reference  = StringField() # id, primary key, indification
    definition = StringField()
    repository = StringField()
    mapping    = StringField() # URL
    # TODO: implement method for parsing path to section
    # or put just a path
    link       = StringField() # PATH
    include    = StringField() # URL

    # collection of section properties
    properties = ListField(EmbeddedDocumentField(Property))

    # private key (hash) of parent section
    parent = StringField()

    # collection of sub-sections
    subsections = ListField(EmbeddedDocumentField(Property))

    # link to previous version of this section
    previous = StringField()