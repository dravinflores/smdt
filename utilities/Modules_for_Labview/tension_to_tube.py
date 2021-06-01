from sMDT import db
from sMDT import tube as Tube
from sMDT.data.tension import TensionRecord

import sys
import datetime


if __name__ == "__main__":
    name = sys.argv[1]
    tension = sys.argv[2]
    frequency = sys.argv[3]
    date = sys.argv[4]
    barcode = sys.argv[5]
    date = datetime.datetime.strptime(date, '%d.%m.%Y %H.%M.%S')

    datab = db.db()
    tube = Tube()
    tube.set_ID(barcode)
    tube.tension.add_record(TensionRecord(tension=tension,
                                          frequency=frequency,
                                          date=date,
                                          user=name))
    datab.add_tube(tube)