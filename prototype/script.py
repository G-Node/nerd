import mongoengine, mapper

# connect to mongo database, nerd collection
mongoengine.connect("nerd")

# insert test document
mapper.save_document("small_example.odml")