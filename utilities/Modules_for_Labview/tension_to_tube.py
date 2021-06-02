from sMDT import db
from sMDT import tube as Tube
from sMDT.data.tension import TensionRecord

import sys
import datetime


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