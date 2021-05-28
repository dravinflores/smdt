Utilites
========
This folder contains a variety of python scripts that provide extra functionality for users of the database. These tend not to be crucial pieces of the process, and are usually just convenient scripts to help in scenarios outside of the regular usage of the database.

Utility|Description
---|---
backup.py|Reads the entire shelved database, and copies it to the backups folder. It then zips the database files into an archive with the date.backup.zip as the filename. Also validates that the copied database is exactly like the original, though this is probably unnecessary and does triple how long it takes.
comment.py|This simple script promps the user for a tube ID, then displays it. The user may then add a comment to the tube, if they so desire. If the user wants, the comment can also mark the tube as as failure.
cleanup.py|This script deletes all files in the new_data and locks directories. This is useful when something goes wrong, and these folders are not properly emptied after a program ends. This is a developer tool, do not run this in the lab without good reason. This will cause major problems if there are programs currently running that are relying on files in these directories.
