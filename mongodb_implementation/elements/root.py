from mongoengine import *
from elements.section import Section

class Root(Document):
    root_id    = IntField()
    # root fields
    author     = StringField()
    date       = StringField()
    repository = StringField()

    # collection of sections that belongs to root
    sections = ListField(StringField())

    # string to produce unique hash
    def __unicode__(self):
        obj_str = str(self.author)     
        obj_str += str(self.date) 
        obj_str += str(self.repository)
        obj_str += str(self.version)
        obj_str += str(self.root_id)

        for sub in self.sections:
            obj_str += sub

        return obj_str

    def get_id(self):
        root_id = hashlib.sha1(str(self)).hexdigest()
        return root_id