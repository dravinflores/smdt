DatabaseManager Application Documentation
=============================
DatabaseManager.py is a crucial piece of the MSU sMDT lab operation. 
This documentation will detail how the software works, how to use it, and why it's necessary.

Why?
------------------
Why is there an extra database manager application that has to constantly run? Why can't the db module just access the database, why do we have to go through this extra process?
The main problem is, only one application/computer can write a file at a time. If they both do, either data will be lost or one/both applications will crash.
We solve this by having an application called the DatabaseManager, who is the only application that ever is allowed to write to the database. 
The functions to write and modify the database are contained in the [db_manager class](db.md), but the DatabaseManager should be the only application that ever calls them.

How?
----
The database manager's primary responsibility is to update the database. It does this by looking inside the [sMDT pachage](sMDT.md) at the new_data directory for files that end in '.tube', which should pickled tube objects. 
It then adds each of these tubes to the database. It also calls the class station_pickler beforehand, which will build these tube objects from data files written by stations. 
Only one instance of DatabaseManager is ever allowed to run at once, and this is assured with the lock system. DatabaseManager will do nothing and print an error message if there is already an instance running. 
It supports several configurations, as described below. 

Config
------
In the main directory, a file called db_config.json tells DatabaseManager.py how to operate. In the actual lab, these should match the value in the Correct Lab State column, but being able to change them is useful for development and testing. 

Key | Description | Correct Lab State
---|---|---
'wipe' |  if true, the database is wiped before DatabaseManager.py is ran. | false
'archive'| Used to set the archive parameter of the db_manager class. For more info, see [db.py documentation](db.md). | true
"loop"| if true, the database manager will loop forever running it's update function, at 5s intervals. Otherwise, it only gets ran once. | true
"cleanup"| If true, it calls the cleanup function of db_manager and locks before it runs. | false