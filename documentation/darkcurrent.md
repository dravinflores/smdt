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

Failure condition: A DarkCurrentRecord is considered a failure if darkcurrent is outside the range (335,365) g.

Member variables|Units|Description
---|---|---
darkcurrent | g | The calculated darkcurrent of the tube.
frequency | #TODO | The measured length from endplug to endplug after swaging is done.
date | datetime | #TODO DOCUMENT ERROR AND CLEAN CODES 
error_code | N/A| #TODO DOCUMENT ERROR AND CLEAN CODES 
date | datetime | the datetime object representing when this was recorded. By default, it's datetime.now() at the point of record creation

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|darkcurrent : float, frequency : float,date : datetime | DarkCurrentRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed tube. See above for description of the failure conditions.

Usage
-----
See the [Station](station.md) documentation for more depth on how to use station objects. 
```python
from sMDT.data import darkcurrent
darkcurrent = darkcurrent.DarkCurrent()                                                #instantiate darkcurrent station object
darkcurrent.set_record(darkcurrent.DarkCurrentRecord(darkcurrent=350, frequency=3.2)) #add 3 DarkCurrentRecords to the darkcurrent station, nonsense values for frequency
darkcurrent.set_record(darkcurrent.DarkCurrentRecord(raw_length=345, frequency=8))
darkcurrent.set_record(darkcurrent.DarkCurrentRecord(raw_length=370, frequency=5))
print(darkcurrent.get_record("first"), darkcurrent.fail("last"))                   #print the first DarkCurrentRecord, and whether the tube fails based on the last record.
```
should output
```
DarkCurrent: 350
Frequency: 3.2
Recorded on: 2021-05-13 14:10:15.074449
Data File: None
True
```
The last true indicates that the last measurement, with a darkcurrent of 370, is too high and therefore is a fail.