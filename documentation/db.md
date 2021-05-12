Database Module Documentation
=============================

sMDT.db is an important module to this library, and serves as the main interface for interaction with the persistent database.

Currently, it stores the database in a local file using the shelve module. You can also specify memory mode, where data is not persisted and is merely stored in memory instead.

Member Function | Parameters | Return Value | Description
---|---|---|---
Constructor | mode='file', path=None | None | Constructs the database object. If mode is 'file', the database will be persisted to the current working directory under database.s