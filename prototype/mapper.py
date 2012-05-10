from odml.tools.xmlparser import load
import elements

# save_document in database
def save_document(file_name):
    root = elements.Root()
    
    odml_file = load(file_name) # load input file: .xml or .odml format
    root.author = odml_file.author
    root.version = odml_file.version
    
    root.save()

    # save first layer of sections
    flat_save(odml_file, root)
    
    # for s in root.sections:
    #     print "x\n"
    #     root.sections.append(str(second_layer_save(s, root)))
    
    # send to database
    root.save()

# takes root - document, save 'first layer' of sections
def flat_save(source, root):
    for sec in source.sections
        : = elements.Section()
        # set default fields
        s.name       = sec.name
        s.type_name  = sec.type
        s.reference  = sec.reference
        s.definition = sec.definition
        s.repository = sec.repository
        s.mapping    = sec.mapping
        s.link       = sec.link
        s.include    = sec.include

        # save properties for that section
        rewrite_properties(sec, s)

        # save sub-section, in second layer
        for section in sec.sections:
            s.sections.append(str(second_layer_save(section, root)))

        # and add to flat section collection
        root.sections.append(s)

# returns id (index in list) of object it creates
def second_layer_save(source, root):
    # create new section object stored in second layer
    s = elements.Section()
    # add custom id
    s.sid = len(root.second_layer)
    # fill section fields
    s.name       = source.name
    s.type_name  = source.type
    s.reference  = source.reference
    s.definition = source.definition
    s.repository = source.repository
    s.mapping    = source.mapping
    s.link       = source.link
    s.include    = source.include

    # save properties for that section
    rewrite_properties(source, s)

    # save sub-sections
    for sec in source.sections:
        s.sections.append(str(second_layer_save(sec, root))) # should work

    # and to second layer
    root.second_layer.append(s)
    
    # return its id
    # return root.second_layer[len(root.second_layer) - 1] # theres is no 'simple' id for embedded document
    return s.sid

# take section as source and save in target(also section)
def rewrite_properties(source, target):
    for pro in source.properties:
        p = elements.Property()
        # save default fields
        name       = pro.name 
        definition = pro.definition
        mapping    = pro.mapping # possible confilct: string list vs sth

        # save all values using external method
        rewrite_values(pro, p)

        # add to targets properties collection
        target.properties.append(p)

# takes properties as arguments
def rewrite_values(source, target):
    # save values from 'values' list and convert to strings objects
    for value in source.values:
        v = elements.Value()
        v.value = str(value._value)
        v.uncertainty = str(value._uncertainty)
        v.unit        = str(value._unit)
        # v.type_name   = str(value.dtype)
        v.definition  = str(value._definition)
        v.reference   = str(value._reference)
        v.filename    = str(value._filename)
        v.encoder     = str(value._encoder)
        v.checksum    = str(value.checksum)
        
        # add crated object to collection
        target.values.append(v)
