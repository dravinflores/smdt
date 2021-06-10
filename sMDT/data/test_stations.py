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
#   Comments: This file had to be recreated. Accidentally deleted.
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
    This test tests the mode system of the station class, and will make a 
    new mode lambda and test it.
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
    This test tests a derived station class, with both built-in and new 
    modes tested.
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
    assert t.get_record(
        lambda x: max(x.m_records, key=lambda y: y.tension)
    ).fail()


def test_swage_status():
    from .swage import Swage, SwageRecord
    from .status import Status
    s = Swage()
    assert s.status() == Status.INCOMPLETE
    s.add_record(SwageRecord(raw_length=-9.71, swage_length=0.07))
    assert s.status() == Status.PASS
    s.add_record(SwageRecord(raw_length=-99999999, swage_length=-0.11))

    # The swage station's fail() method has not been implemented yet. 
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

    # dc.add_record(DarkCurrentRecord(dark_current=0.15))
    dc.add_record(DarkCurrentRecord(dark_current=100))
    assert dc.fail()
    assert dc.status() == Status.FAIL


def test_tension_status():
    from .tension import Tension, TensionRecord
    from .status import Status
    import datetime
    t = Tension()
    assert t.status() == Status.INCOMPLETE
    today = datetime.datetime.now()
    days22 = datetime.timedelta(days=22)
    t.add_record(TensionRecord(tension=350, date=today))
    assert t.status() == Status.PASS
    t.add_record(TensionRecord(tension=350, date=today-days22))
    assert t.status() == Status.PASS

    t2 = Tension()
    t2.add_record(TensionRecord(tension=350, date=today-days22))
    assert t2.status() == Status.PASS


def test_enum():
    from .swage import Swage
    from .status import Status
    swage = Swage()
    assert swage.status() is Status.INCOMPLETE


def test_first_tension():
    from .tension import Tension, TensionRecord
    tStation = Tension()
    assert not tStation.passed_first_tension()
    tStation.add_record(TensionRecord(tension=350))
    assert tStation.passed_first_tension()
    

def test_second_tension():
    from .tension import Tension, TensionRecord
    import datetime
    tStation = Tension()
    assert not tStation.passed_second_tension()
    tStation.add_record(TensionRecord(tension=350))
    assert not tStation.passed_second_tension()
    fifteendays = datetime.timedelta(days=15)
    tStation.add_record(
        TensionRecord(tension=350, date=datetime.datetime.now()-fifteendays)
    )
    assert tStation.passed_second_tension()
