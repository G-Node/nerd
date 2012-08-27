from time import time
from mapper_to_couch import *
import json
import requests 

def test_insertion(count):
    m = CouchMapper()
    
    start = time()

    for x in range (0, count):
        m.root_save('baseline.xml')

    end = time()

    print "Inserted %s documents. Execution time: %s seconds." % (count, end - start)

def test_query(prop, value):

    start = time()
    
    # send query request to database
    r = requests.get("http://localhost:5984/nerd/_design/nerd/_view/emiter?key=[%22" + prop + "%22,%22" + value +"%22]")

    end = time()
    print "Query downloaded. Counting results..."

    count = len(json.loads(r.content)['rows'])
    print "Found %s sections. Execution time: %s seconds." % (count, end - start)

if __name__ == '__main__':
    print "<< COUCH TESTS START >>"

    # TEST INSERTION
    tests = [0] # specify amount of inserted documents here

    for n in tests:
        test_insertion(n)

    # TEST QUERY
    test_query("ResetPotential", "0.0")

    print "<< COUCH TESTS STOP >>"