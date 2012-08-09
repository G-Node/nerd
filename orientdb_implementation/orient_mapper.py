from bulbs.rexster import RexsterClient, Config
import simplejson as sj
from odml.tools.xmlparser import load

def mapper():
    
    config = Config("http://localhost:8182/graphs/orientdbsample", username="admin", password="admin")
    client = RexsterClient(config)

    client.create_vertex(root_to_json('baseline.xml'))

    vertices = client.get_all_vertices()
    res = vertices.get_results()[0]

    for r in res:
        print sj.dumps(r.data, sort_keys=True, indent=4)


def root_to_json(root_input):

    print "mapping.."

    odml_root = load(root_input)

    output = {}

    output['author']     = odml_root.author
    output['date']       = odml_root.date
    output['repository'] = odml_root.repository
    output['version']    = odml_root.version

    #TODO: add sections

    return output

if __name__ == '__main__':
    mapper()