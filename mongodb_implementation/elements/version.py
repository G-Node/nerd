from mongoengine import *

from elements.root import *

class VersionDocument(Document):
    version_id  = IntField()
    author      = StringField()
    date        = DateTimeField()
    root_id     = IntField()
    root_hash   = StringField()

class VersionManager():
    # set properties for version_document and save
    def save_version(self, version, root, author, date):
        v = VersionDocument()
        v.author     = author
        v.date       = date
        v.root_id    = version.version_id
        v.version_id = version.version_id + 1
        v.root_hash  = root.get_id()

        v.save()