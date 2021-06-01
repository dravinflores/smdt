from sMDT import db
from sMDT import tube as Tube
from sMDT.data.leak import LeakRecord

import sys
import datetime


if __name__ == "__main__":
    name = sys.argv[1]
    leak = sys.argv[2]
    pressure = sys.argv[3]
    barcode = sys.argv[4]
    date = sys.argv[5]
    date = datetime.datetime.strptime(date, '%m/%d/%Y%I:%M %p')

    datab = db.db()
    tube = Tube()
    tube.set_ID(barcode)
    tube.leak.add_record(LeakRecord(leak_rate=leak,
                                    date=date, 
                                    user=name))
    datab.add_tube(tube)