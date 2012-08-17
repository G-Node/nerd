from time import time
from mongoengine import connect
import hashlib

from elements.value import Value
from elements.property import Property
from elements.section import *
from versioning import *
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

    # # # test document insertion:
    # for x in range(0,10000):
    #     test_document_insert("baseline.xml")
    
    # test quering database:
    # test_database_queries()
    
    # test_basic_search("NoiseType", "Gaussian")
    
    # test_versioning()

    # test_ids()

    # show_roots()

    # test_version_manager()

    # inspect_collections()

    # map/reduce: not ready yet
    test_map_reduce("NoiseType", "Gaussian")

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
    s = LatestSection()
    s.properties.append(p)
    s2 = LatestSection()
    s2.name = "Tester"
    s.subsections.append(s2.sid())

    print s.sid()
    print s2.sid()

def test_document_insert(file_name):
    m = Mapper()
    m.to_database(file_name)

def test_database_queries():

    def print_sec(sid, ind):
        s = LatestSection.objects(object_id=sid)[0]
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

    for s in LatestSection.objects:
        print s.name + " " + s.object_id + " " + str(s.parent)

def test_basic_search(pro, value):

    query = "{\"properties.name\": \"" + pro + "\"}, {\"properties.values.value\": \"" + value + "\"}"

    result_set = LatestSection.objects(__raw__=eval(query)[0])
    
    # print "---RESULT-SET---"
    # for s in result_set:
    #     print s.id
    # print "----------------"

def test_versioning():
    r = Root.objects()[0]
    print "TESTING VERSIONING: " + str(r.__class__)
    v = Version()
    v.save_root(r)

def test_ids():
    print "IDS: "
    for r in Root.objects():
        print str(r.id) + " : " + str(r.id.__class__)
    print "----"

    x = Root.objects(id="500af779fad9b43fc8000005")[0]
    print x.author

def test_version_manager():
    vm = VersionManager()
    r = Root.objects()[1]
    vm.switch_to_last(r.id)

def show_roots():
    roots = Root.objects()

    for r in roots:
        print "Root { " + str(r.id) + " } -> [ " + str(r.previous) + " ]"

def inspect_collections():
    print "\n\n\nCOLLECTIONS INSPECT\n"

    print "LATEST"
    for s in LatestSection.objects():
        print "Section { " + str(s.object_id) + " : " + str(s.name) +" } "
        for sub in s.subsections:
            print "--> " + sub

    print "\nOLD"
    for s in OldSection.objects():
        print "Section { " + str(s.object_id) + " : " + str(s.name) +" } "
        for sub in s.subsections:
            print "--> " + sub

def test_map_reduce(prop, value):
    db = Connection().nerd
    mapper = Code("""
        function() { 
        var i = this._id; 
        var id = this.object_id; 
        this.properties.forEach(
            function(z) { 
                if (z.name == \"%s\") {
                        var check = false; 
                        z.values.forEach(
                            function(y) {
                                if(y.value == \"%s\") 
                                {
                                    check=true;
                                }
                            }
                        ); 
                        if(check) {
                            emit(i, id);
                        } 
                }
            }
        );
    }""" % (prop, value))

    reducer = Code(""" 
           function (key, values) {

                  return value;
                }
        """)

    result = db.latest_section.map_reduce(mapper, reducer, "myresults")
    # for doc in result.find():
    #     print doc

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