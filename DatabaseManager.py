from sMDT import db
import time
import os



if __name__ == "__main__":
	db_man = db.db_manager()
	current_folder = os.path.dirname(os.path.abspath(__file__))
	db_man.wipe('confirm')
	database = db.db()
	#while True:
	start_time = time.perf_counter()
	db_man.update()
	end_time = time.perf_counter()
	difference_sec = end_time-start_time
	diff_str = str(difference_sec) + " seconds." if difference_sec < 60 else str(difference_sec/60) + " minutes."
	print('Database updated, new size is', str(database.size()) +'.' + "Took", diff_str)
	time.sleep(5)

	