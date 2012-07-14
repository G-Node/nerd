from time import time
from mongoengine import connect
import hashlib

from elements.value import Value
from elements.property import Property
from elements.section import Section
from versioning import Version
from mapper import *

from pymongo import Connection
from bson.code import Code

# main test function
def test():

    # test_value()
    # test_property()
    # test_section()

    # connect with database
    connect("nerd")

    # test document insertion:
    test_document_insert("small_example.odml")
    
    # test quering database:
    # test_database_queries()
    
    # test_basic_search("Grant", "Google")
    
    # test_versioning()

    # map/reduce: not ready yet
    # test_map_reduce("Grant", "Google")

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

def test_document_insert(file_name):
    m = Mapper()
    m.to_database(file_name)

def test_database_queries():

    def print_sec(sid, ind):
        s = Section.objects(object_id=sid)[0]
        if (None == s):
            pass
        else:
            print ind + s.name

            for sec in s.subsections:
                print_sec(sec, ind + "--")

    print "[ sections tree ]"

    roots = Root.objects

    for r in roots:
        for s in r.sections:
            print_sec(s, "")

    print "[ sections in db ]"

    for s in Section.objects:
        print s.name + " " + s.object_id + " " + str(s.parent)

def test_basic_search(pro, value):

    query = "{\"properties.name\": \"" + pro + "\"}, {\"properties.values.value\": \"" + value + "\"}"

    result_set = Section.objects(__raw__=eval(query)[0])
    
    print "---RESULT-SET---"
    for s in result_set:
        print s.id
    print "----------------"

def test_versioning():
    s = Section.objects()[0]
    print s.__class__
    v = Version()
    v.save_section(s)

def test_map_reduce(p, v):
    db = Connection().nerd
    mapper = Code("""
        function () {
        var i = this._id;
        var id = this.object_id;
    
        if (this.isLatest == true) {
            this.properties.forEach(
                function(z) { 
                    if (z.name == \"""" + p + """\" ) {
                        var checkValue = false;
                        z.values.forEach(
                            function(x) {
                                if (x.value == \"""" + v + """\") {
                                    checkValue = true;
                                }
                            }
                        );
        
                        if (checkValue) {
                            emit(i, id);
                        }
                    } 
                } 
            );
        }""")

    reducer = Code(""" 
           function (key, values) {

                  return value;
                }
        """)

    result = db.things.map_reduce(mapper, reducer, "myresults")
    for doc in result.find():
        print doc

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