Leak Module Documentation
==========================

sMDT.data.leak is a module that contains the derived classes of [Station](station.md) and [Record](record.md) for use with the Leak Station. 

This module has two main classes, the Leak object, and the LeakRecord object. The Leak object is a Station that holds a list of LeakRecords.

Leak Station Object
--------------------
leak.Leak, the leak station object, does not do much. All it really does is inherit from [Station](station.md), where all the interesting code is. 

It also provides the \_\_str\_\_ function for printing the station and all of it's records.

LeakRecord Object
------------------
leak.LeakRecord is the [Record](record.md) object that stores a single instance of data from the leak station. 
It's mostly a data container, but provides useful functions for printing and fail testing. 

Failure condition: A LeakRecord is considered a failure if leak is outside the range (335,365) g.

Member variables|Units|Description
---|---|---
leak | g | The calculated leak of the tube.
frequency | #TODO | The measured length from endplug to endplug after swaging is done.
date | datetime | #TODO DOCUMENT ERROR AND CLEAN CODES 
error_code | N/A| #TODO DOCUMENT ERROR AND CLEAN CODES 
date | datetime | the datetime object representing when this was recorded. By default, it's datetime.now() at the point of record creation

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|leak : float, frequency : float,date : datetime | LeakRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed tube. See above for description of the failure conditions.

Usage
-----
See the [Station](station.md) documentation for more depth on how to use station objects. 
```python
from sMDT.data import leak
leak = leak.Leak()                                                #instantiate leak station object
leak.set_record(leak.LeakRecord(leak=350, frequency=3.2)) #add 3 LeakRecords to the leak station, nonsense values for frequency
leak.set_record(leak.LeakRecord(raw_length=345, frequency=8))
leak.set_record(leak.LeakRecord(raw_length=370, frequency=5))
print(leak.get_record("first"), leak.fail("last"))                   #print the first LeakRecord, and whether the tube fails based on the last record.
```
should output
```
Leak: 350
Frequency: 3.2
Recorded on: 2021-05-13 14:10:15.074449
Data File: None
True
```
The last true indicates that the last measurement, with a leak of 370, is too high and therefore is a fail.