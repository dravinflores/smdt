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
    """
    This test is the simplest use case of the library,
    and is the example in README.md
    """
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
    """
    This test tests the mode system of the station class,
    and will make a new mode called highest above and test it.
    """
    from sMDT import tube
    from sMDT.data import tension
    tube1 = tube.Tube()
    tube1.tension.add_record(tension.TensionRecord(350))
    tube1.tension.add_record(tension.TensionRecord(370))
    tube1.tension.add_record(tension.TensionRecord(330))

    assert tube1.tension.get_record(highest).tension == 370


def test_outer_modes():
    '''
    This test tests the mode system of the station class,
    tests records, built-in modes, and user-defined modes.
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
    # assert t.fail()
    assert t.get_record(
            lambda x: max(x.m_records, key=lambda y: y.tension)
    ).tension == 370


def test_outer_swage():
    """
    This test tests the outer library-call use of the swage station.
    """
    from sMDT.data import swage
    # Instantiate swage station object
    swage_station = swage.Swage()

    # Add 3 SwageRecords to the swage station
    swage_station.add_record(swage.SwageRecord(raw_length=3.4, swage_length=3.2))
    swage_station.add_record(swage.SwageRecord(raw_length=5.2, swage_length=8))
    swage_station.add_record(swage.SwageRecord(raw_length=1.03, swage_length=5))

    # Print the first SwageRecord
    assert swage_station.get_record("first").raw_length == 3.4

    # Print whether the tube fails based on the last record.
    assert not swage_station.fail()


def test_outer_tension():
    """
    This test tests the outer library-call use of the tension station.
    """
    from sMDT.data import tension

    # Instantiate tension station object
    tension_station = tension.Tension()

    # Add 3 TensionRecords to the tension station, nonsense values for frequency
    tension_station.add_record(tension.TensionRecord(tension=350, frequency=3.2))
    tension_station.add_record(tension.TensionRecord(tension=345, frequency=8))
    tension_station.add_record(tension.TensionRecord(tension=370, frequency=5))

    # Print the first SwageRecord
    assert tension_station.get_record("first").tension == 350


def test_outer_leak():
    """
    This test tests the outer library-call use of the leak station.
    """
    from sMDT.data import leak

    # print the first SwageRecord

    # Instantiate leak station object
    leak_station = leak.Leak()

    # Add 3 LeakRecords to the leak station, nonsense values for frequency
    leak_station.add_record(leak.LeakRecord(leak_rate=0))
    leak_station.add_record(leak.LeakRecord(leak_rate=5))
    leak_station.add_record(leak.LeakRecord(leak_rate=0.00000000001))

    # Print the first SwageRecord
    assert leak_station.get_record("first").leak_rate == 0

    # Print the first LeakRecord, and whether the tube fails based on the last record.
    assert not leak_station.fail()


def test_outer_darkcurrent():
    """
    This test tests the outer library-call use of the dark current station.
    """
    from sMDT.data import dark_current

    # Instantiate darkcurrent station object
    darkcurrent_station = dark_current.DarkCurrent()

    # Add 3 DarkCurrentRecords to the dark current station,
    # nonsense values for frequency
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(3))
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(1e-10))
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(0))

    # Print the first SwageRecord
    assert darkcurrent_station.get_record("first").dark_current == 3

    # Print the first DarkCurrentRecord, and whether the tube fails
    # based on the last record.
    assert not darkcurrent_station.fail()


def test_comprehensive():
    """
    This comprehensive tests tests several things also tested by other tests,
    but this brings it together and does it with many tubes/records
    """

    from sMDT import db,tube
    from sMDT.data import tension
    tubes = db.db()
    dbman = db.db_manager(testing=True)

    barcode = "MSU00000"
    for i in range(50):
        tube1 = tube.Tube()
        for j in range(i+1):
            tube1.tension.add_record(tension.TensionRecord(j))
        tube1.set_ID(barcode + str(i))
        tubes.add_tube(tube1)

    dbman.update(logging=False)

    assert tubes.get_tube(barcode + str(0)).tension.get_record('first').tension == 0
    assert tubes.get_tube(barcode + str(49)).tension.get_record('last').tension == 49

    del tubes
    tubes = db.db()
    assert tubes.get_tube(barcode + str(0)).tension.get_record('first').tension == 0
    assert tubes.get_tube(barcode + str(49)).tension.get_record('last').tension == 49


def test_db_simple():
    from sMDT import db,tube
    from sMDT.data import tension
    tubes = db.db()
    dbman = db.db_manager(testing=True)
    dbman.wipe('confirm')
    tube1 = tube.Tube()
    barcode = "MSU000001"
    tube1.set_ID(barcode)
    tube1.tension.add_record(tension.TensionRecord(1.5))

    tubes.add_tube(tube1)

    dbman.update(logging=False)

    assert tubes.get_tube(barcode).tension.get_record('first').tension == 1.5


def test_swage_pickler():
    from sMDT import legacy, db
    from sMDT.data.status import Status
    import shelve
    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)

    tube1 = tubes.get_tube("MSU01234")
    assert tube1.get_ID() == "MSU01234"
    assert tube1.swage.get_record().swage_length == 0.07
    assert tube1.swage.get_record().raw_length == -9.71
    assert tube1.swage.status() == Status.PASS


def test_tension_pickler():
    from sMDT import db
    from sMDT.data.status import Status

    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)

    tube1 = tubes.get_tube("MSU01234")
    assert tube1.get_ID() == "MSU01234"
    assert tube1.tension.get_record().tension == 355.448134
    assert tube1.tension.get_record().frequency == 95.0
    assert tube1.tension.status() == Status.PASS


def test_leak_pickler():
    from sMDT import legacy,db
    from sMDT.data.status import Status

    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)

    tube1 = tubes.get_tube("MSU01234")
    assert tube1.get_ID() == "MSU01234"
    assert tube1.leak.get_record().leak_rate == 1.33e-06
    assert not tube1.leak.fail()
    assert tube1.leak.status() == Status.PASS


def test_darkcurrent_pickler():
    from sMDT import db
    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)

    tube1 = tubes.get_tube("MSU01234")
    assert tube1.get_ID() == "MSU01234"
    assert tube1.dark_current.get_record().dark_current == 0


def test_tube_INCOMPLETE_status():
    from sMDT import tube
    from sMDT.data.status import Status
    tube1 = tube.Tube()
    assert tube1.status() == Status.INCOMPLETE


def test_pickled_tube_status():
    from sMDT import db
    from sMDT.data.status import Status
    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)

    tube1 = tubes.get_tube("MSU01234")
    assert tube1.get_ID() == "MSU01234"
    assert tube1.status() == Status.PASS


def test_get_IDs():
    from sMDT import db
    from sMDT.data.status import Status
    db_path = os.path.join(testing_dir, "database.s")
    tubes = db.db(db_path=db_path)

    dbman = db.db_manager(db_path=db_path, testing=False, archive=False)
    dbman.wipe("confirm")
    dbman.cleanup()
    dbman.update(logging=False)

    IDlist = tubes.get_IDs()
    assert IDlist == ["MSU01234"]


def test_db_locking():
    # Currently, as it stands, the database will lock a file called
    # db_lock.lock, and then open up the shelve utility. So the idea is that
    # we should not be able to access that file, until the lock is complete.
    # So, we'll lock that file and make the effort to access it from a
    # different thread.

    import threading
    import time
    from sMDT import db

    database_copy_one = db.db()
    database_copy_two = db.db()

    shelve_dict_one = database_copy_one.open_shelve()
    shelve_dict_two = database_copy_two.open_shelve()

    # TODO: Complete this test


def test_portalocker_locking():
    # The idea here is that we want to see whether portalocker actually
    # locks the file we want it to. So we'll create a file, then check if
    # we can access the file while the lock is still on.
    from pathlib import Path
    import portalocker

    # Here is the path of the file. We're going to assume that this path
    # is in the testing directory.
    lock_file = Path(__file__).resolve() / 'lock_test.lock'
    lock_file.touch(exist_ok=True)

    # Let's go ahead and open the file
    f = lock_file.open('w')

    # Here are the two objects that will attempt to acquire the lock.
    first_locker = portalocker.Lock(f, portalocker.LOCK_EX)
    second_locker = portalocker.Lock(f, portalocker.LOCK_EX)

    # Now let's acquire the first lock.
    first_locker.acquire()

    second_locker_cannot_acquire_lock = False
    try:
        second_locker.acquire()
    except portalocker.exceptions.LockException:
        second_locker_cannot_acquire_lock = True
    finally:
        f.close()

    assert second_locker_cannot_acquire_lock is False
