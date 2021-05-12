Station Module Documentation
=============================

sMDT.data.station is the module that contains the station class, which is the abstract representation for a station.

More specifically, it represents the station as seen by the tube. Each station object is associated with a single tube, and each tube has 4 stations.

A station represents any process of data collection that operates on a particular tube. Currently, the four stations are swage, tension, dark current, and leak. However, there's no reason why it couldn't be expanded into more stations and more data in the future.

A station's main responsibility is to hold a list of records that correspond to tests that the station ran. A record can be of any form, but the Record class sets a standard design for them. They are really just simple data containers, but might also include code like fail() functions.

A station object's job is to keep track of the users that have used the station with that tube, as well as a list of records.

The station *module* also has the ability to define custom modes for the get_record() function and the fail() function.


The Station Class
----------------

Member Variable | Type | Description
---|---|---
m_users | list[string] | A list of every user to use this station with the associated tube. 
m_records | list[Record] | a list of records recorded by the station.

Member Function | Parameters | Return Value | Description
---|---|---|---
Constructor | None | None | Constructs the station object. Empty with no data.
add_user(user)| user : string | None | Adds the new user to the list of users
get_users() | None | list[string] | Returns the list of users
add_record(record) | record : Record | None | Adds the specified record to the list of records
get_record(mode) | mode : string | Record | Returns a single record, as specified by mode. Default mode is 'last',  but see below for documentation on the mode system.
fail(mode) | mode : string | boolean | Returns true if the tube is a failure based on a single record specified by the mode. See below for documentation on the mode system. For the abstract station, this raises NotImplementedError
\_\_str\_\_() | None | string | Raises NotImplementedError
\_\_add\_\_(tube) | tube : Tube | Tube | operator override for '+' operator. You shouldn't use this, it exists so station + station is meaningful when adding tubes together. 

Usage
-----
Below is a simple example of using a class by itself. This example uses integers as its records, but they should be a derived record class in practice.
```python
from sMDT.data import station        #Import station
stat = station.Station()             #Create the station object
stat.add_user("Paul")                #Add the user paul
print(stat.get_users())              #Prints the users. `[Paul]`
stat.add_record(1)                   #Adds an integer record 
stat.add_record(2)
print(stat.get_record(mode='last'))  #Prints whats returned by the get record function, mode being last. The last record added was 2, so it should just print `2`.
```

Mode System
-----------
The mode system is a powerful and convenient solution to some of the the problems we have with accessing our data. More or less all of our stations can record data on a tube multiple times, and our need to save that data has necessitated keeping lists of everything. Furthermore, when we want descriptions or fail() functions that would want a single authoritative value, it makes our programs opaque, inconsistent, and unclear. The mode system improves this, by keeping a set of mode strings that correspond to a particular method of accessing the data. The built-in modes are in the table below, a usage example is above for 'last'. More modes can be dynamically defined by the user. 
Mode name|description
---|---
last|The default mode, this mode simple returns the most recently added record.
first|The opposite of last. Bases the funciton on the first record
Examples:

```python
from sMDT import tube
tube1 = tube.Tube()
```

