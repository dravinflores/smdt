MSU sMDT Documentation
========

sMDT is the Python package built to provide an organized object oriented data structure for applications used in the MSU ATLAS sMDT lab. 
It will also provide a consistent interface for any interactions with the database. 

Structure
--------
* [sMDT](documentation/sMDT.md)
* [sMDT](documentation/sMDT.md)

  * [db](documentation/db.md)

  * [tube](documentation/tube.md)

  * [data](documentation/data.md)

    * [station](documentation/station.md)

    * [swage](documentation/swage.md)

    * [tension](documentation/tension.md)

    * [leak](documentation/leak.md)

    * [darkcurrent](documentation/darkcurrent.md)
 
    * [record](documentation/record.md)

  * [legacy support](documentation/legacy.md)

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
A very simple use case, a simplified tension station.
```python
from sMDT import db,tube                                #import the tube and db modules
from sMDT.data import tension                           #import the tension module
tubes = db.db()                                         #instantiate the database
tube1 = tube.Tube()                                     #make a new tube
tube1.tension.add_record(tension.TensionRecord(1.5))    #Store our new data in the tube, in the form of a TensionRecord object. 
tubes.add_tube(tube1)                                   #Store the tube in the database
```
