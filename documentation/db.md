Database Module Documentation
=============================

[sMDT](sMDT.md).db is an important module to this library, and serves as the main interface for interaction with the persistent database.

The db module is the home of two classes, db and db_manager. An environment with this database consists of one computer/thread that manages the database, and the same computer or any number of additional computers that us the db class to read from the database and interact with the database manager to be able to write.

Without the db_manager running consistently, the database will not be regularly updated and will not work. However, it is extremely important that there is only ever one database manager running at a time. Talk to Paul before touching the db_manager class

Currently, the classes are configured to work around a shelve database in a file all computers see as local (through dropbox, presumably).



db class
--------

Member Function | Parameters | Return Value | Description
---|---|---|---
Constructor | mode : string, path : string | None | Constructs the database object. If a path is provided, it will be used as the path for the shelved database. The default database location is a file named `database.s` in the current working directory.
add_tube(tube) | tube : Tube() | None | Adds the provided tube object to the database. If the tube object is not in the database, it is added. If a tube with a matching ID is already in the database, the tubes are *added together.* The data that the tubes have is merely added together, a tube with 3 tension record plus a tube with 1 tension and a swage record equals a tube with 4 tension records and 1 swage record. --**WARNING**-- do not load a tube from the database, add your data to it, and add that tube back. This will cause it's initial data to be duplicated, since it's being added and it's already there. Instead, make a new tube and set the ID and the data before adding it to the database. \nAdditionally, this data will not be written to the database and be readable by get_tube() until the database manager updates. This should be handled externally in real programs, but for test cases you will need to do it yourself. 
get_tube(id) | id : string | Tube() | Returns the tube with the corresponding id. If no such tube exists, it will raise a KeyError. May wait on a locked database, but delays should be uncommon and short

db_manager class
----------------

Member Function | Parameters | Return Value | Description
---|---|---|---
Constructor | mode : string, path : string | None | Constructs the database manager object. If a path is provided, it will be used as the path for the shelved database. The default database location is a file named `database.s` in the current working directory.
update() | None | None | Updates the database by collecting new tubes marked for adding by the db class (or the station_pickler legacy class) and adding them to the database. The db and pickler classes mark tubes for adding by pickling them into a file that ends in .p and putting them in the directory sMDT/new_data. Locks the database during the write operation. Deletes the pickle files it's done with them.
wipe(confirm) | confirm : string | None | Wipes the database by deleting all the data. **EXTREME CAUTION ADVISED** confirm must be exactly the string "confirm" for wipe to work. 

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
database = db.db()                     #make a new database object, it reads from storage
print(database.get_tube("MSU000001"))  #get the tube we put in before and print it
```
