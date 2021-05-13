Station Module Documentation
=============================

sMDT.data.station is the module that contains the station class, which is the abstract representation for a station.

More specifically, it represents a station as seen by the tube. Each station object is associated with a single tube, and each tube has 4 stations.

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
get_record(mode) | mode : string | Record | Returns a single record, as specified by mode. Default mode is 'last', see below for documentation on the mode system.
fail(mode) | mode : string/function | boolean | Returns true if the tube is a failure based on a single record specified by the mode. Default mode is 'last'. See below for documentation on the mode system. For the abstract station, this raises NotImplementedError
\_\_str\_\_() | None | string | Raises NotImplementedError
\_\_add\_\_(tube) | tube : Tube | Tube | operator override for '+' operator. You shouldn't use this, it exists so station + station is meaningful when adding tubes together. 

Usage
-----
Below is a simple example of using a class by itself. This example uses integers instead of records since the abstract record class doesn't do anything, but it practice it would be a TensionRecord object or similar. They work the same.
```python
from sMDT.data import station,record        #Import station and record
stat = station.Station()             #Create the station object
stat.add_user("Paul")                #Add the user paul
print(stat.get_users())              #Prints the users. `[Paul]`
stat.add_record(1)                   #Adds an integer record 
stat.add_record(2)
print(stat.get_record(mode='last'))  #Prints whats returned by the get record function, mode being last. The last record added was 2, so it should just print `2`.
```

Mode System
-----------
The mode system is a powerful and convenient solution to some of the the problems we have with accessing our data. More or less all of our stations can record data on a tube multiple times, and our need to save that data has necessitated keeping lists of everything. Furthermore, when we want descriptions or fail() functions that would want a single authoritative value, we need to manually code it which makes our programs opaque and inconsistent. The mode system improves this, by keeping a set of built-in modes that can be accessed via strings in the get_record() or fail() function. The built-in modes are in the table below, a usage example is above for 'last'. More modes can be dynamically defined by the user, by passing a function as the mode instead of a string. This function can be a lambda, and must take 1 argument, the station it is operating on. The mode 'last''s corresponding function was implemented just by `lambda x: x.m_records[-1]`.
Mode name|description
---|---
last|The default mode, this mode simple returns the most recently added record.
first|The opposite of last. Bases the funciton on the first record


user defined mode example:

```python
def highest(tension_station):                      #Make a function for our mode, we want get_record to return the record with the highest tension
    max_tension = 0
    max_record = None
    for record in tension_station.m_records:       #simple algorithm to loop through, find the one with the highest tension, and return it.
        if record.tension > max_tension:           #This is just it written out with a real function to simplify it,
            max_tension = record.tension           #but in practice you can shorten this code significantly with lambdas and built-in python functions
            max_record = record                    #the following single line is equivalent to the entire 'highest' function definition
    return max_record                              #highest = lambda tension_station: max(tension_station.m_records, key=lambda tension_record: tension_record.tension)

from sMDT import tube
from sMDT.data import station,tension
tube1 = tube.Tube()
tube1.tension.add_record(tension.TensionRecord(350))
tube1.tension.add_record(tension.TensionRecord(370))
tube1.tension.add_record(tension.TensionRecord(330))
print(tube1.tension.get_record(highest))
```

