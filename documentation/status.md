Status Module
=============

The status module is very simple. All it contains is an Enum class called Status, which gives us a simple and consistent language to talk about the status of a tube or station.

Status
------
Value | Description
---|---
PASS|This means that the tube itself or a particular station is passing.
FAIL|This means that the tube itself or a particular station is failing.
INCOMPLETE|This means that the tube itself or a particular station is incomplete.

Usage
-----
```python
from sMDT import tube                                #import the tube and db modules
tube1 = tube.Tube()
status = tube1.status()                              #Print the tubes status. As this tube has no data, it should return Status.INCOMPLETE
```