from time import time
from mongoengine import connect
from mapper import *
from test_script import test_map_reduce, test_basic_search

def test_insertion(count):
    m = Mapper()
    
    start = time()

    for x in range (0, count):
        m.to_database('baseline.xml')

    end = time()

    print "Inserted %s documents. Execution time: %s seconds." % (count, end - start)

def test_basic_query(pro_name, value_name):
    start = time()
    
    result = test_basic_search(pro_name, value_name)
    
    end = time()    
    
    print "Found %s sections. Execution time: %s seconds." % (result.count(), end - start)

def test_map_reduce_query(pro_name, value_name):
    
    start = time()
    
    result = test_map_reduce(pro_name, value_name)
    
    end = time()
    
    print "Found %s sections. Execution time: %s seconds." % (result.count(), end - start)

if __name__ == '__main__':
    print "<< MONGO TESTS START >>"

    connect('nerd')
    
    numbers = [1, 100, 1000] # specify amount of documents here

    # TESTING INERTIONS
    for n in numbers:
        test_insertion(n)
    
    # TESTING QUERY USING PYTHON DRIVER
    test_basic_query("NoiseType", "Gaussian")

    # TESTING MAP/REDUCE
    test_map_reduce_query("NoiseType", "Gaussian")

    print "<< MONGO TESTS STOP >>"