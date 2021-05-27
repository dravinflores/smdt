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




def test_base_station():
    """
    This test tests the basic functionality of the station class
    Does not use any records or lambdas.
    """
    from .station import Station
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
    from .station import Station
    s = Station()
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
    from .tension import Tension, TensionRecord
    t = Tension()
    t.add_record(TensionRecord(350))
    t.add_record(TensionRecord(330))
    t.add_record(TensionRecord(370))
    t.add_record(TensionRecord(349))
    t.add_record(TensionRecord(351))
    first = t.get_record(mode='first')
    assert first.tension == 350
    assert not first.fail()
    # assert t.fail()
    assert t.get_record(lambda x: max(x.m_records, key=lambda y: y.tension)).fail()


def test_swage_status():
    from .swage import Swage, SwageRecord
    from .status import Status
    s = Swage()
    assert s.status() == Status.INCOMPLETE
    s.add_record(SwageRecord(error_code="0: No Error", raw_length=-9.71, swage_length=0.07))
    assert s.status() == Status.PASS
    s.add_record(SwageRecord(error_code="5: Wire lost inside swaged tube", raw_length=-9.78, swage_length=-0.11))
    assert s.fail()
    assert s.status() == Status.FAIL


def test_leak_status():
    from .leak import Leak, LeakRecord
    from .status import Status
    l = Leak()
    assert l.status() == Status.INCOMPLETE
    l.add_record(LeakRecord(leak_rate=2.56E-07))
    assert l.status() == Status.PASS
    l.add_record(LeakRecord(leak_rate=5))
    assert l.fail()
    assert l.status() == Status.FAIL

def test_dark_current_status():
    from .dark_current import DarkCurrent, DarkCurrentRecord
    from .status import Status
    dc = DarkCurrent()
    assert dc.status() == Status.INCOMPLETE
    dc.add_record(DarkCurrentRecord(dark_current=0))
    assert dc.status() == Status.PASS
    dc.add_record(DarkCurrentRecord(dark_current=0.15))
    assert dc.fail()
    assert dc.status() == Status.FAIL

def test_tension_status():
    from .tension import Tension, TensionRecord
    from .status import Status
    import datetime
    t = Tension()
    assert t.status() == Status.INCOMPLETE
    today = datetime.datetime.now()
    fifteendays = datetime.timedelta(days=15)
    t.add_record(TensionRecord(tension=350, date=today))
    assert t.status() == Status.INCOMPLETE
    t.add_record(TensionRecord(tension=350, date=today-fifteendays))
    assert t.status() == Status.PASS

    t2 = Tension()
    t2.add_record(TensionRecord(tension=350, date=today-fifteendays))
    assert t2.status() == Status.FAIL

def test_enum():
    from .swage import Swage
    from .status import Status
    swage = Swage()
    assert swage.status() is Status.INCOMPLETE

