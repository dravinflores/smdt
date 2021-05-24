from sMDT import db
import time
import os






if __name__ == "__main__":
	db_man = db.db_manager()
	WIPE = False
	wipe = input("Should we wipe the database before this runs? (Y/N), default N\n")
	if wipe.lower() == 'y':
		WIPE = True

	archive = input("Should the database manager delete files from original directories and move them to archive folders? (Y/N), default Y\n")
	ARCHIVE = not archive.lower() == 'n'

	loop = input("Should the database manager repeatedly call update() at 5 second intervals (Y/N), default Y\n")
	LOOP = not loop.lower() == 'n'

	CONTINUE = True
	if not ARCHIVE and LOOP:
		CONTINUE = input("WARNING: NOT ARCHIVING THE FILES AND LOOPING WILL CAUSE THE DATA TO BE ADDED REPEATEDLY ON EVERY UPDATE. Continue? (Y/N)\n")
		if not CONTINUE.lower() == 'y':
			CONTINUE = True

	if CONTINUE:
		
		db_man = db.db_manager(archive=ARCHIVE)
		if WIPE:
			db_man.wipe()
		current_folder = os.path.dirname(os.path.abspath(__file__))
		database = db.db()
		while LOOP:
			start_time = time.perf_counter()
			db_man.update()
			end_time = time.perf_counter()
			difference_sec = end_time-start_time
			diff_str = str(difference_sec) + " seconds." if difference_sec < 60 else str(difference_sec/60) + " minutes."
			print('Database updated, new size is', str(database.size()) +'.' + "Took", diff_str)
			time.sleep(5)
		else:
			start_time = time.perf_counter()
			db_man.update()
			end_time = time.perf_counter()
			difference_sec = end_time-start_time
			diff_str = str(difference_sec) + " seconds." if difference_sec < 60 else str(difference_sec/60) + " minutes."
			print('Database updated, new size is', str(database.size()) +'.' + "Took", diff_str)
			input()
		

	