from odml.tools.xmlparser import load
import couchdb

# class which provides insertion to CouchDB database
class CouchMapper():

    def __init__(self):
        # initialize connection to 'nerd' databse
        couch = couchdb.Server()  
        self.db = couch['nerd']


    # save file to database
    def root_save(self, doc_path):
        # use python-odml driver to load document
        odml_root = load(doc_path)

        # create new dictionary wich will be changed to json by driver
        output = {}
        
        # fill default fields
        output['author']     = odml_root.author
        output['date']       = odml_root.date
        output['repository'] = odml_root.repository
        output['version']    = odml_root.version

        # save root document
        self.db.save(output)

        # save sections using section_save method
        for section in odml_root.sections:
            self.section_save(section)      

    # save section to database
    def section_save(self, source_section):
        
        # dictionary for storing data, same as in root_save
        output = {}
        
        # fill default fields
        output['name']       = source_section.name
        output['type_name']  = source_section.type
        output['reference']  = source_section.reference
        output['definition'] = source_section.definition
        output['repository'] = source_section.repository
        output['mapping']    = source_section.mapping
        output['link']       = source_section.link
        output['include']    = source_section.include
        
        # array to temporary store properties
        properties = []

        # add properties
        for pro in source_section.properties:

            p = {}

            p["name"]            = pro.name 
            p["definition"]      = pro.definition
            p["mapping"]         = pro.mapping 
            p["dependency"]      = pro.dependency
            p["dependencyValue"] = pro.dependency_value

            # for each property add values
            values = []

            for value in pro.values:

                v = {}

                v["value"]       = value.value      
                v["uncertainty"] = value.uncertainty
                v["unit"]        = value.unit       
                v["type_name"]   = value.dtype 
                v["definition"]  = value.definition 
                v["reference"]   = value.reference  
                v["filename"]    = value.filename   
                v["encoder"]     = value.encoder    
                v["checksum "]   = value.checksum

                values.append(v)

            # save values
            p['values'] = values

            properties.append(p)

        # save properties
        output['properties'] = properties

        # send completed document to databse
        self.db.save(output)

        # (recursiv) saving subsections
        for subsection in source_section.sections:
            self.section_save(subsection)
