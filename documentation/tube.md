Tube Module Documentation
=============================

sMDT.tube is the module that contains the Tube class, which is the abstract representation for an tube.

This object only directly holds it's ID and the comments associated with it. It also holds several *Station* objects, one for each station the tube should go through. These station objects are tasked with storing the data associated with that station

Members
----------------

Member Variable | Type | Description
---|---|---
m_tube_id | string | represents the ID number/string of a tube.
m_comments | list[string] | a list of comments associated with the tube
swage | SwageStation | Swage Station object
leak | LeakStation | Leak Station object
tension | TensionStation | Tension Station Object
darkcurrent | DarkCurrentStation | Dark Current Station object

Member Function | Parameters | Return Value | Description
---|---|---|---
Constructor | None | None | Constructs the tube object. Empty with no data or ID, must be set by user. 
new_comment(comment)| comment : string | None | Adds the new comment to the list of comments
get_comments() | None | list[string] | Returns the list of comments
fail() | None | boolean | Returns true if the tube is a failure. A tube is considereed a failure if any of it's station's fail() functions return true. The stations fail functions just use the default mode. 
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