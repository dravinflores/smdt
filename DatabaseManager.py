from sMDT import db
import time
import os

if __name__ == "__main__":
	db_man = db.db_manager()
	current_folder = os.path.dirname(os.path.abspath(__file__))
	db_man.wipe('confirm')
	database = db.db()
	while True:
		db_man.update()
		print('Database updated, new size is', database.size())
		time.sleep(5)

	