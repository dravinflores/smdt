import os
import sys


DROPBOX_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DROPBOX_DIR)

from sMDT import tube,db

import shelve
import zipfile
import datetime


backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backups")

#Credit User Greenstick from stackoverflow https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
def progressBar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


if __name__ == "__main__":
    database1 = db.db()
    database2 = db.db(os.path.join(backup_dir, "database.s"))
    id_list = database1.get_IDs()
    backup_database = shelve.open(os.path.join(backup_dir, "database.s"))
    for id in progressBar(id_list, prefix = 'Backing up database:', suffix = 'Complete', length = 50):
        backup_database[id] = database1.get_tube(id)
    backup_database.close()
    for id in progressBar(id_list, prefix = 'Validating backup:  ', suffix = 'Complete', length = 50):
        assert database1.get_tube(id).status() == database2.get_tube(id).status()
    if not os.path.isdir(backup_dir):
        os.mkdir(backup_dir)
    i = 0
    while True:
        try:
            zip_filename = datetime.date.today().isoformat() + "-" + str(i) + ".backup.zip"
            zf = zipfile.ZipFile(os.path.join(backup_dir, zip_filename), mode='x')
            break
        except FileExistsError:
            i += 1


    zf.write(os.path.join(backup_dir, "database.s.dir"), arcname="database.s.dir")
    zf.write(os.path.join(backup_dir, "database.s.bak"), arcname="database.s.bak")
    zf.write(os.path.join(backup_dir, "database.s.dat"), arcname="database.s.dat")
    zf.close()

    os.remove(os.path.join(backup_dir, "database.s.dir"))
    os.remove(os.path.join(backup_dir, "database.s.dat"))
    os.remove(os.path.join(backup_dir, "database.s.bak"))

    input("Backup done. Press enter to continue...")