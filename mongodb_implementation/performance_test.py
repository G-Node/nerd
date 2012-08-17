from time import time
from mongoengine import connect
from mapper import *

def test_insertion(count):
    m = Mapper()
    
    start = time()

    for x in range (0, count):
        m.to_database('baseline.xml')

    end = time()

    print "Inserted %s documents. Execution time: %s seconds." % (count, end - start)

if __name__ == '__main__':
    print "<< TESTS START >>"

    connect('nerd')
    
    numbers = [1, 10, 100, 1000, 10000] # specify amount of documents here

    for n in numbers:
        test_insertion(n)
    
    print "<< TESTS STOP >>"