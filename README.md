MSU sMDT Python Package
![](https://atlas.cern/sites/atlas-public.web.cern.ch/files/inline-images/ATLAS-Logo-Ref-RGB-H-transparent.png)
========

smdt is the Python package built to provide an organized object oriented data structure for applications used in the MSU ATLAS sMDT lab. 
It will also provide a consistent interface for any interactions with the database. 

Structure
--------

The main concept is the idea of a Tube object. 

Fig. 1
![Fig. 1](https://i.imgur.com/AhDI559.png)
Key:

-Each box is a class

-Arrows represent an "is a" relationship, inheritance. A LeakStation is a type of *Station*

-Italic class names represent an abstract class that should be initialized

-The lines with black diamonds at the end represent a "has a" or an "is made up of" relationship. The numbers represent the multiplicity of the side of the relationship. These are usually member variables.

-A Tube has 1 LeakStation object

-A Leakstation object has a list of LeakRecords 

Installation
------------

Install $project by running:

    install project

Contribute
----------

- Issue Tracker: https://github.com/dravinflores/smdt/issues
- Source Code: https://github.com/dravinflores/smdt

Support
-------

If you are having issues, please let us know.
Talk to Paul or Dravin, or write an issue and put it in the issues section

License
-------

The project is licensed under the GPLv3 license.
