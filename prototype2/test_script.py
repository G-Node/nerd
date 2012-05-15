from time import time
from elements.value import Value
from elements.property import Property

import hashlib

def test():
    # test database here
    # t = 0 
    # for x in range (0,999999):
    #     t += x
    test_value()
    test_property()
    # test, passed without errors

def test_property():
    v = Value()
    v.value = 42
    p = Property()
    p.values.append(v)
    print hashlib.sha1(str(p)).hexdigest()

def test_value():
    v = Value()
    v.value = 108
    v.type_name = "Int"
    print hashlib.sha1(str(v)).hexdigest()

# check how long test was executed
if __name__ == '__main__':
    print "<< START >>"
    start = time()
    # run database tests
    test()
    end = time()
    print "<< STOP >>"
    # print result
    print "Execution time: %s seconds." % (end - start)