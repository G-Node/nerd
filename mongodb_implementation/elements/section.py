from mongoengine import *
import hashlib

from elements.property import Property

# Section is first order document
class Section(Document):
    # primary key
    object_id = StringField()

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

    # flag for latest version of section
    isLatest   = BooleanField()

    # collection of section properties
    properties = ListField(EmbeddedDocumentField(Property))

    # private key (hash) of parent section
    parent = StringField()

    # collection of sub-sections
    subsections = ListField(StringField())

    # string to produce unique hash
    def toString(self):
        obj_str = str(self.name)     
        obj_str += str(self.type_name) 
        obj_str += str(self.reference)
        obj_str += str(self.definition)
        obj_str += str(self.repository)
        obj_str += str(self.mapping)
        obj_str += str(self.link)
        obj_str += str(self.include)

        for prop in self.properties:
            obj_str += str(prop)

        for sub in self.subsections:
            obj_str += sub

        return obj_str

    def sid(self):
        self.object_id = hashlib.sha1(self.toString()).hexdigest()
        return self.object_id