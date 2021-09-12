import sys
import os
import datetime
#DROPBOX_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
#sys.path.append(DROPBOX_DIR)
from sMDT import db
from sMDT import tube as Tube
from sMDT.data.tension import TensionRecord

def main(name, tension, frequency, date, barcode):
    date = datetime.datetime.strptime(date, '%d.%m.%Y %H.%M.%S')

    datab = db.db()
    tube = Tube()
    tube.set_ID(barcode)
    tube.tension.add_record(TensionRecord(tension=tension,
                                          frequency=frequency,
                                          date=date,
                                          user=name))
    datab.add_tube(tube)
