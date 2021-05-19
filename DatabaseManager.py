from sMDT import db
import time
import os

if __name__ == "__main__":
	db_man = db.db_manager()
	current_folder = os.path.dirname(os.path.abspath(__file__))
	#while True:
	db_man.update()
		#time.wait(5)