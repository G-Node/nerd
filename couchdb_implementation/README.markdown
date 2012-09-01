## CouchDB implementation
---

This solution uses Apache Couch database.
Root and sections are separate documents, sections document contains all properties and values.

In order to execute those file, there should be created 'nerd' database.

Easiest way to do that, is to use Futon app: http://localhost:5984/_utils/

For mapping I used couchdb-python driver: http://packages.python.org/CouchDB/getting-started.html

Interaction with view has been done by REST using requests module: http://docs.python-requests.org/en/latest/index.html

---

### Queries setup

For enabling queries: second Map function from file **map_reduce.js** must be saved in Futon manager, as permanent view.
Design document should be named: **"nerd"** and view: **"emiter"**, so it will match witch links names used for pulling queries from database.

(line 23 in *'nerd/couchdb_implementation/performence_test.py'*)

**performance_test.py** use time marks (**start** and **stop**) for counting time needed for fetching all found data, 
from database to program. It not measure time of operations, made on that data. Of course, it could be easily changed, 
simply moving **stop** mark.

Data from CouchDB is fetched in *JSON* format, and then transformed to *python dictionary*, 
by use of **json.loads** method.


---

### Directory structure:

* **mapper_to_couch.py** - provide methods for insertion documents into database.
* **mapreduce.js** - code of two javascript map/reduce functions.
* **view_in_couch.py** - example of fetching couch view.
* **query_on_view** - example of making query on couchdb view (of all property-value pairs)
* **performence_test.py** - script for testing time performence of that implementation.
* other files are example (meta)data files