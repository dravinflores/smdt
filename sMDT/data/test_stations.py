###############################################################################
#   File: test_stations.py
#   Author(s): Paul Johnecheck
#   Date Created: 26 April, 2021
#
#   Purpose: This file is the home of the test cases 
#   on all stations and record keeping withing the tube
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


import pytest

# Import Preparation block.
# Currently only needed so the tests in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)
current_folder = os.path.dirname(os.path.abspath(__file__))

# Adds the folder that file is in to the system path
sys.path.append(current_folder)


def test_base_station():
    """
    This test tests the basic functionality of the station class
    Does not use any records or lambdas.
    """
    from station import Station
    station = Station()
    station.add_record(5)
    station.add_record(3)
    station.add_record(10)
    assert station.get_record("first") == 5
    assert station.get_record("last") == 10
    station.add_record(6)
    assert station.get_record("last") == 6


def test_new_mode():
    """
    This test tests the mode system of the station class, and will make a new mode lambda and test it.
    """
    import station
    s = station.Station()
    s.add_record(5)
    s.add_record(3)
    s.add_record(10)
    s.add_record(3)
    lengthiest = lambda x: max(x.m_records)
    assert s.get_record(lengthiest) == 10


def test_modes_derived_station():
    """
    This test tests a derived station class, with both built-in and new modes tested.
    """
    import tension
    t = tension.Tension()
    t.add_record(tension.TensionRecord(350))
    t.add_record(tension.TensionRecord(330))
    t.add_record(tension.TensionRecord(370))
    t.add_record(tension.TensionRecord(349))
    t.add_record(tension.TensionRecord(351))
    first = t.get_record(mode='first')
    assert first.tension == 350
    assert not first.fail()
    # assert t.fail()
    assert t.get_record(lambda x: max(x.m_records, key=lambda y: y.tension)).fail()


def test_swage_status():
    import swage
    from status import Status
    s = swage.Swage()
    assert s.status() == Status.INCOMPLETE
    s.add_record(swage.SwageRecord(error_code="0: No Error", raw_length=-9.71, swage_length=0.07))
    assert s.status() == Status.PASS
    s.add_record(swage.SwageRecord(error_code="5: Wire lost inside swaged tube", raw_length=-9.78, swage_length=-0.11))
    assert s.fail()
    assert s.status() == Status.FAIL


def test_leak_status():
    import leak
    from status import Status
    l = leak.Leak()
    assert l.status() == Status.INCOMPLETE
    l.add_record(leak.LeakRecord(leak_rate=2.56E-07))
    assert l.status() == Status.PASS
    l.add_record(leak.LeakRecord(leak_rate=5))
    assert l.fail()
    assert l.status() == Status.FAIL

def test_dark_current_status():
    import dark_current
    from status import Status
    dc = dark_current.DarkCurrent()
    assert dc.status() == Status.INCOMPLETE
    dc.add_record(dark_current.DarkCurrentRecord(dark_current=0))
    assert dc.status() == Status.PASS
    dc.add_record(dark_current.DarkCurrentRecord(dark_current=0.15))
    assert dc.fail()
    assert dc.status() == Status.FAIL

def test_tension_status():
    import tension
    from status import Status
    import datetime
    t = tension.Tension()
    assert t.status() == Status.INCOMPLETE
    today = datetime.datetime.now()
    fifteendays = datetime.timedelta(days=15)
    t.add_record(tension.TensionRecord(tension=350, date=today))
    assert t.status() == Status.INCOMPLETE
    t.add_record(tension.TensionRecord(tension=350, date=today-fifteendays))
    assert t.status() == Status.PASS

    t2 = tension.Tension()
    t2.add_record(tension.TensionRecord(tension=350, date=today-fifteendays))
    assert t2.status() == Status.FAIL



if __name__ == "__main__":
    test_modes_derived_station()
    test_new_mode()
    test_base_station()
