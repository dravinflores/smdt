Leak Module Documentation
==========================

[sMDT](sMDT.md).[data](data.md).leak is a module that contains the derived classes of [Station](station.md) and [Record](record.md) for use with the Leak Station. 

This module has two main classes, the Leak object, and the LeakRecord object. The Leak object is a Station that holds a list of LeakRecords.

Leak Station Object
--------------------
leak.Leak, the leak station object, does not do much. All it really does is inherit from [Station](station.md), where all the interesting code is. 

It also provides the \_\_str\_\_ function for printing the station and all of it's records.

LeakRecord Object
------------------
leak.LeakRecord is the [Record](record.md) object that stores a single instance of data from the leak station. 
It's mostly a data container, but provides useful functions for printing and fail testing. 

Failure condition: A LeakRecord is considered a failure if the leak rate is greater than `5.0E-5`

Member variables|Units|Description
---|---|---
leak_rate | #TODO | The measured leak rate of the tube.
date | datetime | the datetime object representing when this was recorded. By default, it's datetime.now() at the point of record creation

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|leak_rate : float, date : datetime, user : string | LeakRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed tube. See above for description of the failure conditions.

Usage
-----
See the [Station](station.md) documentation for more depth on how to use station objects. 
```python
from sMDT.data import leak
leak_station = leak.Leak()                                                #instantiate leak station object
leak_station.set_record(leak.LeakRecord(leak_rate=0)) #add 3 LeakRecords to the leak station, nonsense values for frequency
leak_station.set_record(leak.LeakRecord(leak_rate=5))
leak_station.set_record(leak.LeakRecord(leak_rate=0.00000000001))
print(leak_station.get_record("first"))
print(leak_station.fail("last"))                   #print the first LeakRecord, and whether the tube fails based on the last record.
```
should output
```
Leak Rate: 0
Recorded on: [String representing datetime object of when the record was created]
False
```
The last false indicates that the last measurement, with a leak of 0.00000000001, is low enough to be considered a pass.
