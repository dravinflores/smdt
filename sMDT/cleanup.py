import db

if __name__ == "__main__":
    db_man = db.db_manager()
    db_man.cleanup()
