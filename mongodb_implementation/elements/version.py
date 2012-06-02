from mongoengine import *

from elements.root import *

class Version(Document):
    version_id  = IntField()
    author      = StringField()
    date        = DateTimeField()
    root_id     = IntField()
    root_hash   = StringField()

class VersionManger():
    def save(version, root, author, date):
        v = Version()
        v.author     = author
        v.date       = date
        v.root_id    = version.version_id
        v.version_id = version.version_id + 1
        v.root_hash  = root.get_id()