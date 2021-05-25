Locks Module Documentation
==========================

sMDT.locks is the module that contains the Lock class, a wrapper class for a set of mutual exclusion (mutex) locks.

A mutex lock is useful for a lot of things, primarily enabling communication between threads or programs by locking files or memory writes.

At it's simplest, a mutex lock just tells a program whether a resource is "locked" or not, and then the program should then wait to access that resource until the lock becomes unlocked

Members
-------

Member function | parameters | description
---|---|---
constructor | key : string | A lock object is created, with a particular string key. A key serves to match locks between programs and allow multiple locks to operate simultaneously. The lock for the database.s file is "database". The key is used for a filename, so no disallowed characters or excessively long keys.
lock|None|The Lock becomes locked. (a file [key].lock is written to a folder called 'locks' in the sMDT package)
unlock|None|The lock becomes unlocked. (the file is deleted)
is_locked|None|Return true if the lock is locked, false otherwise 
wait|None|Causes current python process to do nothing (via time.wait(0.5)) until the lock becomes unlocked. If the lock is already locked, it will wait no time and do nothing. 
cleanup | None | Wipes the lock directory, unlocking all locks. This is a static method, you do not have to instantiate a lock to use this. Just locks.Lock.cleanup(). This will cause problems if ran during normal execution, but it's helpful when programs crash during development and leave some files locked. Do not call if you don't know what you're doing. 
