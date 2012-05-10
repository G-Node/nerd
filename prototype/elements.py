from mongoengine import *

''' 
    Documents classes, bottom to up order.
    All field types should be reconsiderd.
'''
class Value(EmbeddedDocument):
    # value fields
    value       = StringField()
    uncertainty = StringField()
    unit        = StringField()
    # type_name   = StringField()
    definition  = StringField()
    reference   = StringField()
    filename    = StringField()
    encoder     = StringField()
    checksum    = StringField()

class Property(EmbeddedDocument):
    # property fields
    name            = StringField()
    definition      = StringField()
    mapping         = ListField(StringField()) # string ??
    dependency      = ListField(StringField()) # properties ids ??
    dependencyValue = StringField()   
    
    # collection of values 
    values = ListField(EmbeddedDocumentField(Value))

class Section(EmbeddedDocument):
    # neccessary id, implemented as index in second_layer list
    sid = IntField()
    
    # section fields
    name       = StringField()
    type_name  = StringField()
    reference  = StringField()
    definition = StringField()
    repository = StringField()
    mapping    = ListField(StringField()) # string list ??
    link       = StringField()
    include    = StringField()
    
    # collection of subsections ids
    sections = ListField(StringField())
    # collection of properties
    properties   = ListField(EmbeddedDocumentField(Property))

class Root(Document):
    # root fields
    author     = StringField()
    # date       = StringField()
    repository = StringField()
    version    = StringField()
    
    # main (flat - first layer) collection of sections
    sections = ListField(EmbeddedDocumentField(Section))
    
    # collection of inner sections
    second_layer = ListField(EmbeddedDocumentField(Section))
