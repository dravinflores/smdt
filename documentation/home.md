MSU sMDT Documentation
========

sMDT is the Python package built to provide an organized object oriented data structure for applications used in the MSU ATLAS sMDT lab. 
It will also provide a consistent interface for any interactions with the database. 

Structure
--------
When building Python libraries, they are made up of Packages and Modules. Packages are folders that can contain modules, and modules are python code files that can contain classes and functions. Both can be imported. 
The main sMDT package and the data package are the only packages, the rest are modules and the description is about the classes inside them. 

* [sMDT](sMDT.md) -main Package

  * [db](db.md) -database interface object

  * [tube](tube.md) -Tube object 
  * [data](data.md) -data Package

    * [station](station.md) -abstract base class for a station

    * [swage](swage.md) -swage station and swage record

    * [tension](tension.md) -Tension station and tension record

    * [leak](leak.md) -Leak station and leak record

    * [dark_current](darkcurrent.md) -Dark current station and dark current record
 
    * [record](record.md) -abstract base class for a record

  * [legacy support](legacy.md)

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
