Tension Module Documentation
==========================

[sMDT](sMDT.md).[data](data.md).tension is a module that contains the derived classes of [Station](station.md) and [Record](record.md) for use with the Tension Station. 

This module has two main classes, the Tension object, and the TensionRecord object. The Tension object is a Station that holds a list of TensionRecords.

Tension Station Object
--------------------

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|None|None|Constructs the tension station object
passed_first_tension()|None|Bool|Returns true if the tension station has any passing tension records.
passed_second_tension()|None|Bool|Returns true if the tension station has a pair of passing tension records that were recorded at least a week apart.
status()|None|Status|Returns Status.PASS if the tube has passed its second tension. If it has no records, or if the first passing record was less than two weeks ago, returns Status.INCOMPLETE. Otherwise, returns Status.FAIL
fail()|None|bool|Returns True if this data indicates a failed tube. This is equivalent to status() == Status.FAIL.

TensionRecord Object
------------------
tension.TensionRecord is the [Record](record.md) object that stores a single instance of data from the tension station. 
It's mostly a data container, but provides useful functions for printing and fail testing. 

Failure condition: A TensionRecord is considered a failure if tension is outside the range (335,365) g.

Member variables|Units|Description
---|---|---
tension | g | The calculated tension of the tube.
frequency | #TODO | The measured length from endplug to endplug after swaging is done.
date | datetime | the datetime object representing when this was recorded. By default, it's datetime.now() at the point of record creation

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|tension : float, frequency : float, date : datetime, user : string | TensionRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed record. See above for the failure condition.

Usage
-----
See the [Station](station.md) documentation for more depth on how to use station objects. 
```python
from sMDT.data import tension
tStation = tension.Tension()                                                #instantiate tension station object
tStation.set_record(tension.TensionRecord(tension=350, frequency=3.2))      #add 3 TensionRecords to the tension station, nonsense values for frequency
tStation.set_record(tension.TensionRecord(raw_length=345, frequency=8))
tStation.set_record(tension.TensionRecord(raw_length=370, frequency=5))
print(tStation.get_record("first"))                                         #print the first TensionRecord, and whether the tube fails based on the last record.
print(tStation.status())                                                    #Print this tube's status. 
```   
should output
```
Tension: 350
Frequency: 3.2
Recorded on: [String representing datetime object of when the record was created]
Status.INCOMPLETE
```
This tube is incomplete because while it does not have two passing tensions that are two weeks apart, it's first passing test is within two weeks ago. (Unless it took a ***REALLY*** long time to run some of those lines)
