Locks Module Documentation
==========================

sMDT.locks is the module that contains the Lock class, a wrapper class for a set of mutual exclusion (mutex) locks.

A mutex lock is useful for a lot of things, primarily enabling communication between threads or programs by locking files or memory writes.

At it's simplest, a mutex lock just tells a program whether a resource is "locked" or not, and then the program should then wait to access that resource until the lock becomes unlocked

Members
-------

Member function | parameters | description
---|---|---
constructor | key : string | a lock object is created, with a particular string key. A key serves to match locks between programs and allow multiple to operate simultaneously. the lock for the database.s file is "database" it's used for a filename, so no disallowed character or excessively long strings.
lock|None|the Lock becomes locked. (a file [key].lock is written to a folder called Locks in the sMDT package)
unlock|None|the lock becomes unlocked. (the file is deleted)
is_locked|None|return true if the lock is locked, false otherwise 
wait|None|causes current python process to do nothing (via time.wait(0.5)) until the lock becomes unlocked. If the lock is already locked, it will wait no time and do nothing. 