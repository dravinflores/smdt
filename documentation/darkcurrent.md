DarkCurrent Module Documentation
==========================

sMDT.data.darkcurrent is a module that contains the derived classes of [Station](station.md) and [Record](record.md) for use with the DarkCurrent Station. 

This module has two main classes, the DarkCurrent object, and the DarkCurrentRecord object. The DarkCurrent object is a Station that holds a list of DarkCurrentRecords.

DarkCurrent Station Object
--------------------
darkcurrent.DarkCurrent, the darkcurrent station object, does not do much. All it really does is inherit from [Station](station.md), where all the interesting code is. 

It also provides the \_\_str\_\_ function for printing the station and all of it's records.

DarkCurrentRecord Object
------------------
darkcurrent.DarkCurrentRecord is the [Record](record.md) object that stores a single instance of data from the darkcurrent station. 
It's mostly a data container, but provides useful functions for printing and fail testing. 

Failure condition: A DarkCurrentRecord is considered a failure if darkcurrent is greater than 1 nA.

Member variables|Units|Description
---|---|---
dark_current | nA | The measured dark current of the tube.
date | datetime | the datetime object representing when this was recorded. By default, it's datetime.now() at the point of record creation

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|darkcurrent : float, date : datetime | DarkCurrentRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed tube. See above for description of the failure conditions.

Usage
-----
See the [Station](station.md) documentation for more depth on how to use station objects. 
```python
from sMDT.data import dark_current
darkcurrent_station = dark_current.DarkCurrent()                      #instantiate DarkCurrent station object
darkcurrent_station.add_record(dark_current.DarkCurrentRecord(3))     #add 3 DarkCurrentRecords to the darkcurrent station, nonsense values for frequency
darkcurrent_station.add_record(dark_current.DarkCurrentRecord(1e-10))
darkcurrent_station.add_record(dark_current.DarkCurrentRecord(0))
print(darkcurrent_station.get_record("first"))
print(darkcurrent_station.fail("last"))                               #print the first DarkCurrentRecord, and whether the tube fails based on the last record.

```
should output
```
Dark Current: 3
Recorded on: 2021-05-13 14:37:30.246337
Data File: None
False
```
The last false indicates that the last measurement, with a darkcurrent of 0, passes the test.