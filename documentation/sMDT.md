sMDT Package Documentation
==========================

sMDT is the base Python package that the library is built around. All interaction with the library and the database will be inside the sMDT package.

sMDT is a Python package, which is really just a folder for organizing pieces of Python code called modules. sMDT contains several modules and one sub-package, as detailed and documented below

* [db](db.md) -Database module

* [tube](tube.md) -Tube object representation

* [data](data.md) -Package

  * [station](station.md) -Abstract base class for a station

  * [swage](swage.md) -Swage station and swage record

  * [tension](tension.md) -Tension station and tension record

  * [leak](leak.md) -Leak station and leak record

  * [dark_current](darkcurrent.md) -Dark current station and dark current record
 
  * [record](record.md) -Abstract base class for a record

* [legacy support](legacy.md)

UML Class Diagram
![](https://i.imgur.com/g7Dv28C.png)

Usage
-----
The sMDT package does not have any of its own code, but is a container for other modules. To access those modules, you must import them.
```python
import sMDT
databaseObject = sMDT.db.db()		#see db documentation
myTube = sMDT.tube.tube()		#see tube documentation
```
Also acceptable is the this alternative syntax
```python
from sMDT import db,tube
databaseObject = db.db()
myTube = tube.Tube()
```


