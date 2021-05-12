Database Module Documentation
=============================

sMDT.db is an important module to this library, and serves as the main interface for interaction with the persistent database.

Currently, it stores the database in a local file using the shelve module. You can also specify memory mode, where data is not persisted and is merely stored in memory instead.

Member Function | Parameters | Return Value | Description
---|---|---|---
Constructor | mode='file', path=None | None | Constructs the database object. If mode is 'file', the database will be persisted to the filesystem. If mode is 'mem', it only uses memory. Otherwise, an error is raised. If a path is provided, it will be used as the path for the shelved database.