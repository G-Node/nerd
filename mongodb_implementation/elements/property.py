from mongoengine import *
from elements.value import Value

class Property(EmbeddedDocument):
    # property fields
    name            = StringField()
    definition      = StringField()
    mapping         = StringField() # URL
    # TODO: implement method for property validation (in Section)
    
    # python-odml assume that it's just a one dependency
    dependency      = StringField()
    dependencyValue = StringField()   
    
    # collection of values 
    values = ListField(EmbeddedDocumentField(Value))

    # string to produce unique hash
    def __unicode__(self):
        obj_str = str(self.name)
        obj_str += str(self.definition)
        obj_str += str(self.mapping)
        obj_str += str(self.dependency)
        obj_str += str(self.dependencyValue)

        for v in self.values:
            obj_str += str(v)

        return obj_str