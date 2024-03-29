Legacy Support
==============

One challenge involved with implementing a database like this is actually moving to it from an old system. 

To that end, the sMDT.legacy module contains functions for migrating from the old system. 

station_pickler class
---------------------
The station pickler class's job is to prepare data into a pickled tube file format from legacy systems that build CSVs.
There are four functions in station_pickler, one corresponding with swage, leak, darkcurrent, and tension stations. 
A function in this class pulls data from their respective data folders, and reformats it into a pickled tube.
It then archives the original csv file if it was instructed to.

Member Function | parameter | description
---|---|---
Constructor|path : string, archive : bool, logging : bool| Constructs the station_pickler object. path needs to be a path to the directory containing the sMDT library and the various station folders. The archive parameter defines what this class will do with the data files it reads, and defaults to true. In the real lab environment, archive needs to be true. When db_manager.update() is ran repeatedly and calls this class repeatedly, all the data will get added to the database multiple times. Archiving fixes this by deleting the files from the original folder and moving them to an archive folder, when they wont be read next time. When testing and developing though, having to rebuild the source database each time you want to test is very tedious, so archive being false stops that behaviour. Be warned: if db_manager.update() repeatedly runs when archive is false, then the database balloon up as duplicate data is read in indefinetely. If logging is true (by default), then the program will output many lines that correspond to what it's doing via print(). 
pickle_swage|None|Loops through all the '.csv' data that was generated by the old swage station, building pickled tube files out of them for db_manager to read. The SwagerStation folder in the lab's base directory contains 'SwagerData', the source of the old data. If archive is on, the csvs will get deleted from 'SwagerData' and moved to the 'archive' folder in the same directory. The swage station itself now uses the db class, so this function should only be necessary for old data. 
pickle_tension|None|Loops through all the csv data that was generated by the tension station, building pickled tube files out of them for db_manager to read. The TensionStation folder in the lab's base directory contains 'output', the source of the data. If archive is on, the files will get deleted from 'output' and moved to the 'archive' folder in the same directory.
pickle_leak|None|Loops through all the '.txt' data that was generated by the leak station, building pickled tube files out of them for db_manager to read. The LeakDetector folder in the lab's base directory is the source of the data. If archive is on, the files will get deleted from 'LeakDetector' and moved to the 'archive' folder in the directory LeakStation. The archive directory is in a different folder, but the folder LeakDetector was required by the old station. Making the leak station write to LeakStation/LeakData is an eventual goal for the purpose of consistent organization.
pickle_darkcurrent|None|Loops through all the '.csv' data that was generated by the dark current station, building pickled tube files out of them for db_manager to read. The 'DarkCurrent/3015V Dark Current' directory is the source of the data. If archive is on, the files will get deleted from there and moved to the 'archive' folder in the directory DarkCurrentStation. The archive directory is in a different folder, but the format was required by the old station much like Leak. Making the station write to DarkCurrentStation/DarkCurrentData is an eventual goal for the purpose of consistent organization.
write_errors | None | As each station runs, the station_pickler class keeps a python set for each one. The pickler adds to the set any filename that caused it to skip any data contained therein. write_errors writes the contents of these sets to a file in the base directory called 'errors.txt'
