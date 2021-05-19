Record Module Documentation
===========================

[sMDT](sMDT.md).[data](data.md).Record is an abstract base class for a single piece of rcorded data.

Currently, this class does nothing but provide a template for Records used by stations. It just keeps the user's name and all it's functions just raise NotImplementedError.

Members
-------

Member variables | Type | Description
---|---|---
user | string | String representing the name of the user that created the associated record. None if none recorded.

Member functions | Parameters | Return | Description
---|---|---|---
fail()|None|boolean|A record should implement a fail() function. This raises NotImplementedError
\_\_str\_\_()|None|string|Records should be able to be represented as a string by implementing this function. Raises NotImplementedError.

