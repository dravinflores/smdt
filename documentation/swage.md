Swage Module Documentation
==========================

[sMDT](sMDT.md).[data](data.md).swage is a module that contains the derived classes of [Station](station.md) and [Record](record.md) for use with the Swage Station. 

This module has two main classes, the Swage object, and the SwageRecord object. The Swage object is a Station that holds a list of SwageRecords.

Swage Station Object
--------------------
swage.Swage, the swage station object, does not do much. All it really does is inherit from [Station](station.md), where all the interesting code is. 

It also provides the \_\_str\_\_ function for printing the station and all of it's records.

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|None|None|Constructs the swage station object
status()|None|[Status](status.md)|Returns Status.INCOMPLETE if there is no records. If there is a record with no error codes and within the constraints, returns Status.PASS. Otherwise, returns Status.FAIL
fail()|None|bool|Returns True if this data indicates a failed tube. This is equivalent to status() == Status.FAIL.
\_\_str\_\_()|None|string|Returns a string representation of the station

SwageRecord Object
------------------
swage.SwageRecord is the [Record](record.md) object that stores a single instance of data from the swage station. 
It's mostly a data container, but provides useful functions for printing and fail testing. 

Member variables|Units|Description
---|---|---
raw_length | cm | The measured length of the tube before it is swaged. 
swage_length | cm| The measured length from endplug to endplug after swaging is done.
clean_code | N/A| #TODO DOCUMENT ERROR AND CLEAN CODES 
error_code | N/A| #TODO DOCUMENT ERROR AND CLEAN CODES 
date | datetime | the datetime object representing when this was recorded. By default, it's datetime.now() at the point of record creation

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|raw_length : float, swage_length : float,clean_code : string, error_code : string, date : datetime, user : string| SwageRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed tube. See above for the failure condition. 

Usage
-----
See the [Station](station.md) documentation for more depth on how to use station objects. 
```python
from sMDT.data import swage
swage_station = swage.Swage()                                                #instantiate swage station object
swage_station.add_record(swage.SwageRecord(raw_length=3.4, swage_length=3.2))#add 3 SwageRecords to the swage station
swage_station.add_record(swage.SwageRecord(raw_length=5.2, swage_length=8))
swage_station.add_record(swage.SwageRecord(raw_length=1.03, swage_length=5))
print(swage_station.get_record("first"))                                     #print the first SwageRecord
print(swage_station.fail("last"))                                            #print wether the tube fails based on the last record.
```
should output
```
Raw Length: 3.4
Swage Length: 3.2
Clean Code: None
Error Code: None
Recorded on: [String representing datetime object of when the record was created]
False
```
The last false being that a tube with a raw length of 1.03 cm does not fail according to our current failure conditions. They should be looked at.
