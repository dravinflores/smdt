from sMDT import db
from sMDT import tube as Tube
from sMDT.data.dark_current import DarkCurrentRecord

import sys
import datetime


if __name__ == "__main__":
    name = sys.argv[1]
    dark_current = sys.argv[2]
    date = sys.argv[3]
    barcode = sys.argv[4]
    date = datetime.datetime.strptime(date, '%m/%d/%Y%I:%M %p')

    datab = db.db()
    tube = Tube()
    tube.set_ID(barcode)
    tube.leak.add_record(DarkCurrentRecord(dark_current=dark_current,
                                           date=date, 
                                           user=name))
    datab.add_tube(tube)