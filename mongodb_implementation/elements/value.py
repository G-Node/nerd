from mongoengine import EmbeddedDocument, StringField

class Value(EmbeddedDocument):
    # value fields
    value       = StringField()
    uncertainty = StringField()
    unit        = StringField()
    type_name   = StringField()
    definition  = StringField()
    reference   = StringField()
    filename    = StringField()
    encoder     = StringField()
    checksum    = StringField()

    # string to produce unique hash
    def __unicode__(self):
        obj_str = str(self.value)
        obj_str += str(self.uncertainty)
        obj_str += str(self.unit)
        obj_str += str(self.type_name)
        obj_str += str(self.definition)
        obj_str += str(self.reference)
        obj_str += str(self.filename)
        obj_str += str(self.encoder)
        obj_str += str(self.checksum)
        return obj_str