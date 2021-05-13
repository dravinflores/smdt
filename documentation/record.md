Record Module Documentation
===========================

Currently, this class does nothing but provide a template for Records used by stations. It does nothing by itself, and all it's functions just raise NotImplementedError.

Member functions | Parameters | Return | Description
---|---|---|---
fail()|None|boolean|A record should implement a fail() function. This raises NotImplementedError
\_\_str\_\_()|None|string|Records should be able to be represented as a string by implementing this function. Raises NotImplementedError.

