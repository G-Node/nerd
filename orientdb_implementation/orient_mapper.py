from bulbs.rexster import RexsterClient, Config
import simplejson as sj
from odml.tools.xmlparser import load

from time import time

class Mapper():

    def __init__(self):
        config = Config("http://localhost:8182/graphs/orientdbsample", username="admin", password="admin")
        self.client = RexsterClient(config)

        for x in range(0, 10):
            self.root_save('small_example.odml')

    def show_vertices(self):
        vertices = client.get_all_vertices()
        res = vertices.get_results()[0]
    
        for r in res:
            print sj.dumps(r.data, sort_keys=True, indent=4)
    

    def root_save(self, root_input):
    
        # print "mapping.."
    
        odml_root = load(root_input)
    
        output = {}
    
        output['author']     = odml_root.author
        output['date']       = odml_root.date
        output['repository'] = odml_root.repository
        output['version']    = odml_root.version
    
        r_id = ((self.client.create_vertex(output)).get_results()[0]).get_id()

        # print "Root ID = " + r_id

        for section in odml_root.sections:
            s_id = self.section_save(section)
            self.client.create_edge(r_id, "root-section", s_id)
            self.client.create_edge(s_id, "section-root", r_id)
    
    
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

            # print "property.."

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

        section_id = ((self.client.create_vertex(output)).get_results()[0]).get_id()

        for subsection in source_section.sections:
            s_id = self.section_save(subsection)
            self.client.create_edge(section_id, "section-section", s_id)
            self.client.create_edge(s_id, "section-section", section_id)

        return section_id

if __name__ == '__main__':

    print "<< ORIENT START >>"
    start = time()
    
    m = Mapper()
    
    end = time()
    print "<< ORIENT STOP >>"
    
    print "Execution time: %s seconds." % (end - start)