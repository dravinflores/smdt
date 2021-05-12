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
fail() | None | boolean | Returns true if the tube is a failure. A tube is considereed a failure if any of it's station's fail() functions return true. The stations fail functions just use the default mode. 
\_\_str\_\_() | None | string | Raises NotImplementedError
\_\_add\_\_(tube) | tube : Tube | Tube | operator override for '+' operator. You shouldn't use this, it exists so station + station is meaningful when adding tubes together. 

Usage
-----
Below is a simple example of using the tube class.
```python
from sMDT import tube                                #import the tube module
from sMDT.data import tension                        #import the tension module
tube1 = tube.Tube()                                  #make a new tube object
tube1.m_id = "MSU000001"                             #set it's ID
tube1.tension.add_record(tension.TensionRecord(1.5)) #see the station and the tension module for explanation of this line
tube1.new_comment("This tube is an example")         #add a comment