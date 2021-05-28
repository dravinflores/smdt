MSU sMDT Database Systems
========
![](https://atlas.cern/sites/atlas-public.web.cern.ch/files/inline-images/ATLAS-Logo-Ref-RGB-H-transparent.png)

This directory contains all the code, programs, and data used in the MSU ATLAS sMDT lab. 
It consists of several python and labview applications that act as stations in our lab, which each record data on tubes.
Recording the data and storing it is handled by the sMDT python package. 

Structure
--------
Here are the important components of the computer systems at the lab.

Component | Description
---|---
[sMDT](documentation/sMDT.md) | This folder is a python package that handles all database access. Further documentation can be found on that page.
[DatabaseManager.py](documentation/DatabaseManager.md) | This program is the database manager, and it's designed to loop in the background and keep the database up to date. Only one may be running at a time. It should automatically stop a second instance from running, but if they start at close to the same time it might not work. Just don't run this program unless you have a good reason for it.
db_config.json | This json file represents a dictionary, where the each key being true or false corresponds with particular behavior. This is the configuration file for [DatabaseManager.py](documentation/DatabaseManager.md). See its documentation for further information. 
[utilities](documentation/utilities.md) | This folder contains several handy python scripts. See it's documentation for more information. 
testing | This folder contains a python module with automated test cases, as well as the small-scale full lab testing environment it needs.
Station folders | For each station, there is one or two folders associated with them. For swage and tension, there is one directory called [station name]Station that holds both data output by the station and archived past output. Due to legacy requirements, leak and dark_current have different folders for their output, but their archive is in their respective [StationName]Station folder.
Export_tubes.py | This gui allows the user to scan in a set of tubes that will be shipped to UofM, and the program will output particular data we have on them that is of use to UofM.
errors.txt | This file is a text record of files that the station_pickler had issues with. 

Data Flow
---------
![](https://imgur.com/a/TNRzhpA)

Documentation
-------------
Be sure to read the [documentation for the sMDT package](documentation/sMDT.md) before working with the sMDT computer systems.

Examples
--------
A very simple use case, such as at the tension station. For this code to work without any changes to the system path, the py script containing this snippet needs to be in the same directory the sMDT package (folder) is in.
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
Talk to Paul, Dravin, Jason, or any of our successors. Alternatively, write an issue and put it in the issue tracker. 
