Database Module Documentation
=============================

sMDT.db is an important module to this library, and serves as the main interface for interaction with the persistent database.

Currently, it stores the database in a local file using the shelve module. You can also specify memory mode, where data is not persisted and is merely stored in memory instead.

The main (and only) feature of this module is the db class, described below.

Member Functions
----------------
Member Function | Parameters | Return Value | Description
---|---|---|---
Constructor | mode : string, path : string | None | Constructs the database object. Default mode is 'file', If mode is 'file', the database will be persisted to the filesystem. If mode is 'mem', it only uses memory. Otherwise, an error is raised. If a path is provided, it will be used as the path for the shelved database. The default database location is a file named `database.s` in the current working directory.
add_tube(tube) | tube : Tube() | None | Adds the provided tube object to the database. If the tube object is not in the database, it is added. If a tube with a matching ID is already in the database, the tubes are *added together.* The data that the tubes have is merely added together, a tube with 3 tension record plus a tube with 1 tension and a swage record equals a tube with 4 tension records and 1 swage record. --**WARNING**-- do not load a tube from the database, add your data to it, and add that tube back. This will cause it's initial data to be duplicated, since it's being added and it's already there. Instead, make a new tube and set the ID and the data before adding it to the database.  
get_tube(id) | id : string | Tube() | Returns the tube with the corresponding id. If no such tube exists, it will raise a KeyError
wipe() | None | None | Wipes the database by deleting all the data. **EXTREME CAUTION ADVISED**	

Usage
-----
Below is a simple example of using the db class.
```python
from sMDT import db,tube               #import the modules
database = db.db()                     #initialize the database object
tube1 = tube.Tube()                    #make a new tube object
tube1.m_id = "MSU000001"               #set it's ID
database.add_tube(tube1)               #add the tube to the database
del database                           #delete the database object from memory, does not effect file storage.
database = db.db()	                   #make a new database object, it reads from storage
print(database.get_tube("MSU000001"))  #get the tube we put in before and print it
```