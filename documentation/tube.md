Tube Module Documentation
=============================

[sMDT](sMDT.md).tube is the module that contains the Tube class, which is the abstract representation for an tube.

This object only directly holds it's ID and the comments associated with it. It also holds several [Station](station.md) objects, one for each station the tube should go through. These station objects are tasked with storing the data associated with that station

Members
----------------

Member Variable | Type | Description
---|---|---
m_tube_id | string | represents the ID number/string of a tube. Use getters and setters rather than direct access.
m_comments | list[string] | a list of comments associated with the tube.  Use getters and setters rather than direct access.
swage | [SwageStation](swage.md) | Swage Station object
leak | [LeakStation](leak.md) | Leak Station object
tension | [TensionStation](tension.md) | Tension Station Object
darkcurrent | [DarkCurrentStation](darkcurrent.md) | Dark Current Station object
legacy_data | dict() | A generic dictionary for arbitrary data associated with legacy operations. Most likely empty. Only current key is "is_munich", a true or false value representing whether the munich type of endplug was used for this tube. 

Member Function | Parameters | Return Value | Description
---|---|---|---
Constructor | None | None | Constructs the tube object. Empty with no data or ID, must be set by user. 
new_comment(comment)| comment : string | None | Adds the new comment to the list of comments
get_comments() | None | list[string] | Returns the list of comments
get_ID(),set_ID(ID) | None, ID | string, None | Simple getter and setter for the tube's ID.
fail() | None | boolean | Returns true if the tube is a failure. A tube is considereed a failure if any of it's station's fail() functions return true. The stations fail functions just use the default mode. 
status() | None | [Status Enum](status.md) | Returns an Enum representing the status of a tube. A tube is either a Status.PASS, a Status.FAIL, or a Status.INCOMPLETE. status() will return Status.FAIL IF AND ONLY IF fail() returns True.  
\_\_str\_\_() | None | string | returns string representation of the tube.
\_\_add\_\_(tube) | tube : Tube | Tube | operator override for '+' operator. You shouldn't use this, it exists so tube + tube is meaninful when adding to the database. 


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
