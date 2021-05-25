MSU sMDT Database Systems
![](https://atlas.cern/sites/atlas-public.web.cern.ch/files/inline-images/ATLAS-Logo-Ref-RGB-H-transparent.png)
========

This directory contains all the code, programs, and data used in the MSU ATLAS sMDT lab. 
It consists of several python and labview applications that act as stations in our lab, which each record data on tubes.
Recording the data and storing it is handled by the sMDT python package. 

Structure
--------
Here are the important components of the computer systems at the lab.

Component | Description
---|---
[sMDT](documentation/sMDT.md) | This folder is a python packagethat handles all database access. Further documentation can be found on that page.
DatabaseManager.py | This program is the database manager, and it's designed to loop in the background and keep the database up to date. Probably should be moved to the package directory. 
db_config.json | This json file represents a dictionary with 4 keys, each corresponding to a boolean. This is the configuration file for [DatabaseManager.py](documentation/databasemanager.md). See its documentation for further information. 
test_outer.py | A python module containing automated test cases. 
Station folders | For each station, there is one or two folders associated with them. For swage and tension, there is one directory called [station name]Station that holds both data output by the station and archived past output. Due to legacy requirements, leak and dark_current have different folders for their output, but their archive is in their respective [StationName]Station folder.
Export_tubes.py | This gui allows the user to scan in a set of tubes that will be shipped to UofM, and the program will output particular data we have on them that is of use to UofM.

Key | Description
---|---
'wipe' |  if true, the database is wiped before DatabaseManager.py is ran. Should be false for real-world lab use.
'archive'| Used to set the archive parameter of the db_manager class. For more info, see [db.py documentation](documentation/db.md).
"loop"| if true, the database manager will loop forever running it's update function, at 5s intervals. Otherwise, it only gets ran once.
"cleanup"| If true, it calls the cleanup function of db_manager and locks before it runs. MUST BE FALSE FOR LAB. **ONLY** make this true if you are developing and understand what it does.

Documentation
-------------
Full documentation can be found in [our documentation folder](documentation/home.md)

Installation
------------
Visit the following link for the source code.

https://github.com/dravinflores/smdt

As of now, this library is not uploaded to PyPi or a similar python package manager for easy installation with like `pip install sMDT`.
Maybe it will be eventually, but for now you just have to install it manually. 

The easiest way to do it is to just download the sMDT folder from the above github and just put it in the current working directory (same folder) of the code you're executing. A below example will show you how to import it, but it should just work if the sMDT *folder* is in the same folder as your code.

It's also possible to add it to the python path somehow, or move it to a location already on the path. That will be left as an excercise for the reader. 

Examples
--------
A very simple use case, such as at the tension station.
```python
from sMDT import db,tube                                #import the tube and db modules
from sMDT.data import tension                           #import the tension module
tubes = db.db()                                         #instantiate the database
tube1 = tube.Tube()                                     #make a new tube
tube1.tension.add_record(tension.TensionRecord(350))    #Store our new data in the tube, in the form of a TensionRecord object. 
tubes.add_tube(tube1)                                   #Store the tube in the database
```

Contribute
----------

- Issue Tracker: https://github.com/dravinflores/smdt/issues
- Source Code: https://github.com/dravinflores/smdt

Support
-------

If you are having issues, please let us know.
Talk to Paul or Dravin, or write an issue and put it in the issue tracker
