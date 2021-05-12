###############################################################################
#   File: test_stations.py
#   Author(s): Paul Johnecheck
#   Date Created: 02 April, 2021
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
# Currently only needed so the records in the mains work with the current imports.
import os
import sys

# Gets the path of the current file being executed.
path = os.path.realpath(__file__)

# Adds the folder that file is in to the system path
sys.path.append(path[:-len(os.path.basename(__file__))])


def test_base_station():
    '''
    This test tests the basic functionality of the station class
    Does not use any records or lambdas. 
    '''
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
    '''
    This test tests the basic functionality of the station class
    Does not use any records or lambdas. 
    '''
    import station
    s = station.Station()
    s.add_record(5)
    s.add_record(3)
    s.add_record(10)
    s.add_record(3)
    lengthiest = lambda x: max(x.m_records)
    assert s.get_record(lengthiest) == 10

def test_modes_derived_station():
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
    assert not t.fail(mode='first')
    import station
    assert t.fail(lambda x: max(x.m_records, key=lambda y: y.tension))
    t.get_record(mode=lambda x: x.m_records)
    print(t.get_record('all'))





if __name__ == "__main__":
    test_modes_derived_station()