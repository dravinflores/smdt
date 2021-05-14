Data Package Documentation
==========================

data is the Python sub-package that holds the pieces of the library that have to do with stations and data recording/management.
The two main abstractions are the Station and Record class, and the four stations each inherit their own versions of these two classes.

Modules:
--------
* [station](station.md) -Abstract base class for a station

* [record](record.md) -Abstract base class for a record

* [swage](swage.md) -Swage station and swage record

* [tension](tension.md) -Tension station and tension record

* [leak](leak.md) -Leak station and leak record

* [dark_current](darkcurrent.md) -Dark current station and dark current record
 

Usage
-----
The data package does not have any of its own code, but is a container for other modules. To access those modules, you must import them.
```python
from sMDT.data import tension
myRecord = tension.TensionRecord(1.5)
```



