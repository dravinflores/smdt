import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sMDT import db, locks
import time


if __name__ == "__main__":
	lock = locks.Lock("database_manager")
	if lock.is_locked():
		print("There can only be one Database Manager running at a time!")
		input("Press enter to continue...")
	else:
		WIPE = False
		ARCHIVE = True
		LOOP = True
		CLEANUP = False
		NOPICKLER = True

		db_man = db.db_manager(archive=ARCHIVE, testing=NOPICKLER)
		if WIPE:
			db_man.wipe('confirm')
			db_man.cleanup()
		if CLEANUP:
			db_man.cleanup()

		lock.lock()
		current_folder = os.path.dirname(os.path.abspath(__file__))
		database = db.db()

		while LOOP:
			start_time = time.perf_counter()
			db_man.update()
			end_time = time.perf_counter()
			elapsed = end_time - start_time

			print_str = f"Database updated. Updated size is {database.size()}. "
			print_str += f"This took {elapsed:0.2f} seconds."
			print(print_str)
			time.sleep(5)
		else:
			start_time = time.perf_counter()
			db_man.update()
			end_time = time.perf_counter()
			elapsed = end_time - start_time

			print_str = f"Database updated. Updated size is {database.size()}. "
			print_str += f"This took {elapsed:0.2f} seconds."
			print(print_str)
			lock.unlock()
		input("Press enter to continue...")
		

	
