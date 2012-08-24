## CouchDB implementation
---

This solution uses Apache Couch database.
Root ans sections are separate documents, sections document contains all properties and values.

In order to execute those file, there should be created 'nerd' database.
Easiest way to do that, is to use Futon app: http://localhost:5984/_utils/

For mapping I used couchdb-python driver: http://packages.python.org/CouchDB/getting-started.html
Interaction with view has been done by REST using requests moduel: http://docs.python-requests.org/en/latest/index.html
---

### Directory structure:

* **mapper_to_couch.py** - provide methods for insertion documents into database.
* **mapreduce.js** - example of featching javascript map/reduce view.
* **performence_test.py** - script for testing time performence of that implementation.
* other files are example (meta)data files