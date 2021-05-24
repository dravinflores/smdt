from sMDT import db
import time
import os
import json





if __name__ == "__main__":


	f = open("db_config.json", 'r')
	config = json.load(f)
	f.close()

	WIPE = config['wipe']
	ARCHIVE = config['archive']
	LOOP = config['loop']
	CLEANUP = config['cleanup']

	


	db_man = db.db_manager(archive=ARCHIVE)
	if WIPE:
		db_man.wipe()
		db_man.cleanup()
	if CLEANUP:
		db_man.cleanup()
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

		

	