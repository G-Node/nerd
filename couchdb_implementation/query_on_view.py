from time import time
import requests 
from awesome_print import ap
import json

start = time()

prop = "TestPro1"
value = "TestValue1"

# send query request to database
r = requests.get("http://localhost:5984/nerd/_design/nerd/_view/emiter?key=[%22" + prop + "%22,%22" + value +"%22]") 

end = time()
print "-->|"

# ap(r.content) # print results

count = len(json.loads(r.content)['rows'])
print "Found %s sections. Execution time: %s seconds." % (count, end - start)