Tension Module Documentation
==========================

sMDT.data.tension is a module that contains the derived classes of [Station](station.md) and [Record](record.md) for use with the Tension Station. 

This module has two main classes, the Tension object, and the TensionRecord object. The Tension object is a Station that holds a list of TensionRecords.

Tension Station Object
--------------------
tension.Tension, the tension station object, does not do much. All it really does is inherit from [Station](station.md), where all the interesting code is. 

It also provides the \_\_str\_\_ function for printing the station and all of it's records.

TensionRecord Object
------------------
tension.TensionRecord is the [Record](record.md) object that stores a single instance of data from the tension station. 
It's mostly a data container, but provides useful functions for printing and fail testing. 

Failure condition: A TensionRecord is considered a failure if tension is outside the range (335,365) g.

Member variables|Units|Description
---|---|---
tension | g | The calculated tension of the tube.
frequency | #TODO | The measured length from endplug to endplug after swaging is done.
date | datetime | #TODO DOCUMENT ERROR AND CLEAN CODES 
error_code | N/A| #TODO DOCUMENT ERROR AND CLEAN CODES 
date | datetime | the datetime object representing when this was recorded. By default, it's datetime.now() at the point of record creation

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|tension : float, frequency : float,date : datetime | TensionRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed tube. See above for description of the failure conditions.

Usage
-----
See the [Station](station.md) documentation for more depth on how to use station objects. 
```python
from sMDT.data import tension
tension = tension.Tension()                                                #instantiate tension station object
tension.set_record(tension.TensionRecord(tension=350, frequency=3.2)) #add 3 TensionRecords to the tension station, nonsense values for frequency
tension.set_record(tension.TensionRecord(raw_length=345, frequency=8))
tension.set_record(tension.TensionRecord(raw_length=370, frequency=5))
print(tension.get_record("first"), tension.fail("last"))                   #print the first TensionRecord, and whether the tube fails based on the last record.
```
should output
```
Tension: 350
Frequency: 3.2
Recorded on: 2021-05-13 14:10:15.074449
Data File: None
True
```
The last true indicates that the last measurement, with a tension of 370, is too high and therefore is a fail.