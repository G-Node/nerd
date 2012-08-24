from time import time
import requests 
from awesome_print import ap
import json

start = time()
r = requests.get('http://localhost:5984/nerd/_design/nerd/_view/mapred')
end = time()
print "-->|"
count = len(json.loads(r.content)['rows'])
print "Found %s sections. Execution time: %s seconds." % (count, end - start)