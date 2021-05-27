###############################################################################
#   File: test_outer.py
#   Author(s): Paul Johnecheck
#   Date Created: 02 May, 2021
#
#   Purpose: This file is the home of the test cases 
#   that will import the library just like a user/application will.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

import os
import sys

testing_dir = os.path.dirname(os.path.abspath(__file__))
dropbox_dir = os.path.dirname(testing_dir)
sys.path.append(dropbox_dir)

def test_outer():
    '''
    This test is the simplest use case of the library, and is the example in README.md
    '''
    from sMDT import db,tube
    from sMDT.data import tension
    tubes = db.db()
    tube1 = tube.Tube()
    tube1.tension.add_record(tension.TensionRecord(1.5))
    assert tube1.tension.get_record().tension == 1.5

def highest(tension_station):
    max_tension = 0
    max_record = None
    for record in tension_station.m_records:
        if record.tension > max_tension:
            max_tension = record.tension
            max_record = record
    return max_record

def test_user_defined_mode():
    '''
    This test tests the mode system of the station class, and will make a new mode called highest above and test it.
    '''
    from sMDT import tube
    from sMDT.data import station,tension
    tube1 = tube.Tube()
    tube1.tension.add_record(tension.TensionRecord(350))
    tube1.tension.add_record(tension.TensionRecord(370))
    tube1.tension.add_record(tension.TensionRecord(330))
    assert tube1.tension.get_record(highest).tension == 370

def test_outer_modes():
    '''
    This test tests the mode system of the station class, tests records, built-in modes, and user-defined modes.
    '''
    from sMDT.data import tension,station
    t = tension.Tension()
    t.add_record(tension.TensionRecord(350))
    t.add_record(tension.TensionRecord(330))
    t.add_record(tension.TensionRecord(370))
    t.add_record(tension.TensionRecord(349))
    t.add_record(tension.TensionRecord(351))
    first = t.get_record(mode='first')
    assert first.tension == 350
    assert not first.fail()
    #assert t.fail()
    assert t.get_record(lambda x: max(x.m_records, key=lambda y: y.tension)).tension == 370

def test_outer_swage():
    '''
    This test tests the outer library-call use of the swage station.
    '''
    from sMDT.data import swage
    swage_station = swage.Swage()                                                #instantiate swage station object
    swage_station.add_record(swage.SwageRecord(raw_length=3.4, swage_length=3.2))#add 3 SwageRecords to the swage station
    swage_station.add_record(swage.SwageRecord(raw_length=5.2, swage_length=8))
    swage_station.add_record(swage.SwageRecord(raw_length=1.03, swage_length=5))
    assert swage_station.get_record("first").raw_length == 3.4                              #print the first SwageRecord
    assert not swage_station.fail()                                         #print wether the tube fails based on the last record.


def test_outer_tension():
    '''
    This test tests the outer library-call use of the tension station.
    '''
    from sMDT.data import tension
    tension_station = tension.Tension()                                                #instantiate tension station object
    tension_station.add_record(tension.TensionRecord(tension=350, frequency=3.2)) #add 3 TensionRecords to the tension station, nonsense values for frequency
    tension_station.add_record(tension.TensionRecord(tension=345, frequency=8))
    tension_station.add_record(tension.TensionRecord(tension=370, frequency=5))
    assert tension_station.get_record("first").tension == 350                              #print the first SwageRecord
    #assert tension_station.fail()                   #print the first TensionRecord, and whether the tube fails based on the last record.

def test_outer_leak():
    '''
    This test tests the outer library-call use of the leak station.
    '''
    from sMDT.data import leak
    leak_station = leak.Leak()                                                #instantiate leak station object
    leak_station.add_record(leak.LeakRecord(leak_rate=0)) #add 3 LeakRecords to the leak station, nonsense values for frequency
    leak_station.add_record(leak.LeakRecord(leak_rate=5))
    leak_station.add_record(leak.LeakRecord(leak_rate=0.00000000001))
    assert leak_station.get_record("first").leak_rate == 0                            #print the first SwageRecord
    assert not leak_station.fail()                   #print the first LeakRecord, and whether the tube fails based on the last record.

def test_outer_darkcurrent():
    '''
    This test tests the outer library-call use of the dark current station.
    '''
    from sMDT.data import dark_current
    darkcurrent_station = dark_current.DarkCurrent()                                                #instantiate darkcurrent station object
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(3)) #add 3 DarkCurrentRecords to the darkcurrent station, nonsense values for frequency
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(1e-10))
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(0))
    assert darkcurrent_station.get_record("first").dark_current == 3                              #print the first SwageRecord
    assert not darkcurrent_station.fail()                   #print the first DarkCurrentRecord, and whether the tube fails based on the last record.


def test_comprehensive():
    '''
    This comprehensive tests tests several things also tested by other tests, but this brings it together and does it with many tubes/records
    '''

    from sMDT import db,tube
    from sMDT.data import tension
    tubes = db.db()
    dbman = db.db_manager(testing=True)
    
    id = "MSU00000"
    for i in range(50):
        tube1 = tube.Tube()
        for j in range(i+1):
            tube1.tension.add_record(tension.TensionRecord(j))
        tube1.set_ID(id + str(i))
        tubes.add_tube(tube1)

    dbman.update(logging=False)

    assert tubes.get_tube(id + str(0)).tension.get_record('first').tension == 0
    assert tubes.get_tube(id + str(49)).tension.get_record('last').tension == 49

    del tubes
    tubes = db.db()
    assert tubes.get_tube(id + str(0)).tension.get_record('first').tension == 0
    assert tubes.get_tube(id + str(49)).tension.get_record('last').tension == 49

def test_db_simple():
    from sMDT import db,tube
    from sMDT.data import tension
    tubes = db.db()
    dbman = db.db_manager(testing=True)
    dbman.wipe('confirm')
    tube1 = tube.Tube()
    id = "MSU000001"
    tube1.set_ID(id)
    tube1.tension.add_record(tension.TensionRecord(1.5))

    tubes.add_tube(tube1)

    dbman.update(logging=False)

    assert tubes.get_tube(id).tension.get_record('first').tension == 1.5

def test_swage_pickler():
    from sMDT import legacy,db
    import shelve
    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)


    tube1 = tubes.get_tube("MSU01447")
    assert tube1.get_ID() == "MSU01447"
    assert tube1.swage.get_record().swage_length == 0.07
    assert tube1.swage.get_record().raw_length == -9.71

def test_tension_pickler():
    from sMDT import legacy,db
    import shelve
    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)


    tube1 = tubes.get_tube("MSU02458")
    assert tube1.get_ID() == "MSU02458"
    assert tube1.tension.get_record().tension == 355.448134
    assert tube1.tension.get_record().frequency == 95.0

def test_leak_pickler():
    from sMDT import legacy,db
    import shelve
    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)


    tube1 = tubes.get_tube("MSU03026")
    assert tube1.get_ID() == "MSU03026"
    assert tube1.leak.get_record().leak_rate == 1.33e-06
    assert not tube1.leak.fail()

def test_darkcurrent_pickler():
    from sMDT import legacy,db
    import shelve
    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)

    tube1 = tubes.get_tube("MSU02673")
    assert tube1.get_ID() == "MSU02673"
    assert tube1.dark_current.get_record().dark_current == -.15

def test_tube_INCOMPLETE_status():
    from sMDT import tube
    from sMDT.data.status import Status
    tube1 = tube.Tube()
    assert tube1.status() == Status.INCOMPLETE

