Swage Module Documentation
==========================

sMDT.data.swage is a module that contains the derived classes of [Station](station.md) and [Record](record.md) for use with the Swage Station. 

This module has two main classes, the Swage object, and the SwageRecord object. The Swage object is a Station that holds a list of SwageRecords.

Swage Station Object
--------------------
swage.Swage, the swage station object, does not do much. All it really does is inherit from [Station](station.md), where all the interesting code is. 

It also provides the __str__ function for printing the station and all of it's records.

SwageRecord Object
------------------
swage.SwageRecord is the [Record](record.md) object that stores a single instance of data from the swage station. 
It's mostly a data container, but provides useful functions for printing and fail testing. 

Failure condition: A SwageRecord is considered a failure if raw_length is outside the range (0,2000) cm, or if the swage_length is outside the same range.

The failure condition may not be accurate, #TODO

Member variables|Units|Description
---|---|---
raw_length | cm | The measured length of the tube before it is swaged. 
swage_length | cm| The measured length from endplug to endplug after swaging is done.
clean_code | N/A| #TODO DOCUMENT ERROR AND CLEAN CODES 
error_code | N/A| #TODO DOCUMENT ERROR AND CLEAN CODES 

Member Functions|Parameters|Return|Description
---|---|---|---
Constructor|raw_length : float, swage_length : float,clean_code : string, error_code : string | SwageRecord object | Creates a record object with the specified data
\_\_str\_\_()|None|string|Returns a string representation of the record
fail()|None|bool|Returns True if this data indicates a failed tube. See above for description of the failure conditions.  