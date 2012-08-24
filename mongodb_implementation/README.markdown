## MongoDB implementation
---

Every section is independent document that have array of subsection id's. (hash)
Roots are in separate collection, they point to their (direct) sections.

Sections are splited into two collections:
* *latest_sections* - default collection for newly created section
* *old_sections* - contains previous versions of sections from latest_sections collections

All queries are executed only on latest_sections collection.

For mapping I used mongoengine python driver: http://mongoengine.org/

---

### Directory structure:

* ***elements*** - contains set of class, that represents odml structure.
* **mapper.py** - provide methods for insertion documents into database.
* **mapreduce.js** - example of pure javascript map/reduce query.
* **test_script.py** - provides functions for testing all functionality that was included.
* **versioning.py** - contains class for saving database verion, and for manage that process.
* **performence_test.py** - script for testing time performence of that implementation.
* other files are example (meta)data files