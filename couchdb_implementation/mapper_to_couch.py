from odml.tools.xmlparser import load
from time import time
import simplejson as sj
import couchdb

class CouchMapper():

    def __init__(self):
        couch = couchdb.Server()
        self.db = couch['nerd']

    def root_save(self, doc_path):
        odml_root = load(doc_path)

        output = {}
    
        output['author']     = odml_root.author
        output['date']       = odml_root.date
        output['repository'] = odml_root.repository
        output['version']    = odml_root.version

        self.db.save(output)

        for section in odml_root.sections:
            self.section_save(section)      


    def section_save(self, source_section):
    
        output = {}
    
        output['name']       = source_section.name
        output['type_name']  = source_section.type
        output['reference']  = source_section.reference
        output['definition'] = source_section.definition
        output['repository'] = source_section.repository
        output['mapping']    = source_section.mapping
        output['link']       = source_section.link
        output['include']    = source_section.include
        
        properties = []

        for pro in source_section.properties:

            p = {}

            p["name"]            = pro.name 
            p["definition"]      = pro.definition
            p["mapping"]         = pro.mapping 
            p["dependency"]      = pro.dependency
            p["dependencyValue"] = pro.dependency_value

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

            p['values'] = values

            properties.append(p)

        output['properties'] = properties

        self.db.save(output)

        for subsection in source_section.sections:
            self.section_save(subsection)

if __name__ == '__main__':

    print "<< COUCH START >>"
    start = time()
    
    m = CouchMapper()
    m.root_save("baseline.xml")

    end = time()
    print "<< COUCH STOP >>"
    
    print "Execution time: %s seconds." % (end - start)