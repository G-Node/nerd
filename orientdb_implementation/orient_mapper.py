from bulbs.rexster import RexsterClient, Config
import simplejson as sj
from odml.tools.xmlparser import load

class Mapper():

    def __init__(self):
        config = Config("http://localhost:8182/graphs/orientdbsample", username="admin", password="admin")
        self.client = RexsterClient(config)

        self.root_save('small_example.odml')

    def show_vertices(self):
        vertices = client.get_all_vertices()
        res = vertices.get_results()[0]
    
        for r in res:
            print sj.dumps(r.data, sort_keys=True, indent=4)
    

    def root_save(self, root_input):
    
        print "mapping.."
    
        odml_root = load(root_input)
    
        output = {}
    
        output['author']     = odml_root.author
        output['date']       = odml_root.date
        output['repository'] = odml_root.repository
        output['version']    = odml_root.version
    
        r_id = ((self.client.create_vertex(output)).get_results()[0]).get_id()

        print "Root ID = " + r_id

        for section in odml_root.sections:
            s_id = self.section_save(section)
            self.client.create_edge(r_id, "root-section", s_id)
    
    
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

        section_id = ((self.client.create_vertex(output)).get_results()[0]).get_id()
    
        for subsection in source_section.sections:
            s_id = self.section_save(subsection)
            self.client.create_edge(section_id, "section-section", s_id)

        return section_id

if __name__ == '__main__':
    m = Mapper()