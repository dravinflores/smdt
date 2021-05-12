sMDT Package Documentation
==========================

sMDT is the base Python package that the library is built around. All interaction with the library and the database will be through the sMDT package, likely starting with `from sMDT import *`

sMDT is a Python packae, which is really just a folder for organizing pieces of Python code called Modules. sMDT has several modules and one sub-package, as detailed and documented below

* [db](documentation/db.md)

* [tube](documentation/tube.md)

* [data](documentation/data.md)

  * [station](documentation/station.md)

  * [swage](documentation/swage.md)

  * [tension](documentation/tension.md)

  * [leak](documentation/leak.md)

  * [darkcurrent](documentation/darkcurrent.md)
 
  * [record](documentation/record.md)

* [legacy support](documentation/legacy.md)

Usage
-----
The sMDT package does not have any of its own code, but is a container for other modules. To access those modules, you must import them.
```python
import sMDT
databaseObject = sMDT.db.db()	#see db documentation
myTube = sMDT.tube.tube()		#see tube documentation
```