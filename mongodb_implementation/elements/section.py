from mongoengine import *
import hashlib

from elements.property import Property

class RecursiveObject(EmbeddedDocument):
    obj = EmbeddedDocumentField('self')

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


    # collection of sub-sections
    # 'self' - means recursive embedded document
    subsections = ListField(ReferenceField(Section))

    # link to previous version of this section
