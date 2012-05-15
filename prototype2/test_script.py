from time import time
from elements.value import Value

def test():
    # test database here
    v = Value()
    
    # t = 0 
    # for x in range (0,999999):
    #     t += x
    
    print ("It works!")

# check how long test was executed
if __name__ == '__main__':
    start = time()
    # run database test
    test()
    end = time()
    # print result
    print "Execution time: %s seconds." % (end - start)