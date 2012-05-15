from mongoengine import EmbeddedDocument, StringField

class Value(EmbeddedDocument):
    value       = StringField()
    uncertainty = StringField()
    unit        = StringField()
    type_name   = StringField()
    definition  = StringField()
    reference   = StringField()
    filename    = StringField()
    encoder     = StringField()
    checksum    = StringField()