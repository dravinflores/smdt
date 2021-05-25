MSU sMDT Database Systems
![](https://atlas.cern/sites/atlas-public.web.cern.ch/files/inline-images/ATLAS-Logo-Ref-RGB-H-transparent.png)
========

This directory contains all the code, programs, and data used in the MSU ATLAS sMDT lab. 
It consists of several python and labview applications that act as station in our lab, which each record data on tubes.
Recording the data and storing it is handled by the sMDT python package. 

Structure
--------



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
