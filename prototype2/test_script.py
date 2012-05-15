from elements.value import Value
from elements.property import Property
from elements.section import Section

from time import time
import hashlib

# main test function
def test():
    # test database here
    # t = 0 
    # for x in range (0,999999):
    #     t += x
    
    # test_value()
    # test_property()
    test_section()

def test_property():
    v = Value()
    v.value = 41
    p = Property()
    p.values.append(v)
    print hashlib.sha1(str(p)).hexdigest()

def test_value():
    v = Value()
    v.value = 108
    v.type_name = "Int"
    print hashlib.sha1(str(v)).hexdigest()

def test_section():
    v = Value()
    v.value = 42
    p = Property()
    p.values.append(v)
    s = Section()
    s.properties.append(p)
    s2 = Section()
    s2.name = "Tester"
    s.subsections.append(s2.sid())

    print s.sid()
    print s2.sid()

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