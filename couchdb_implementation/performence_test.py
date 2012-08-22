from time import time
from mapper_to_couch import *

def test_insertion(count):
    m = CouchMapper()
    
    start = time()

    for x in range (0, count):
        m.root_save('baseline.xml')

    end = time()

    print "Inserted %s documents. Execution time: %s seconds." % (count, end - start)

if __name__ == '__main__':
    print "<< COUCH TESTS START >>"

    numbers = [1, 10, 100] # specify amount of documents here

    # TESTING INERTIONS
    for n in numbers:
        test_insertion(n)

    print "<< COUCH TESTS STOP >>"