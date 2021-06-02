###############################################################################
#   File: test_tube_db.py
#   Author(s): Paul Johnecheck
#   Date Created: 2 May, 2021
#
#   Purpose: This file is the home of the test cases 
#   for the tube and the db classes.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

import pytest


def test_tube_init():
    '''
    Testing tube initialization and constructor
    '''
    from . import tube
    from .data import swage, tension, leak, dark_current
    tube1 = tube.Tube()
    assert tube1.m_comments == []
    assert tube1.m_tube_id == None
    assert tube1.swage.get_record('all') == []
    assert tube1.tension.get_record('all') == []
    assert tube1.dark_current.get_record('all') == []
    assert tube1.leak.get_record('all') == []


def test_tube_comments():
    '''
    Simple test of the comment system
    '''
    from . import tube
    tube1 = tube.Tube()
    tube1.new_comment("This tube is for testing purposes")
    assert tube1.get_comments() == ["This tube is for testing purposes"]


def test_tube_add():
    '''
    This tests the __add__ override that tubes support.
    '''
    from . import tube
    from .data import swage, tension, leak, dark_current
    tube1 = tube.Tube()
    tube2 = tube.Tube()
    tube1.set_ID("MSU0000001")
    tube2.set_ID("MSU0000001")
    tube1.tension.add_record(tension.TensionRecord(350, user='Paul'))
    tube2.tension.add_record(tension.TensionRecord(355, user='Reinhard'))
    tube2.leak.add_record(leak.LeakRecord(0))
    tube3 = tube1 + tube2
    assert len(tube3.tension.get_record('all')) == 2
    assert tube3.leak.get_record('last').leak_rate == 0
    assert tube3.tension.get_record('last').user == 'Reinhard'
    assert tube3.tension.get_record('first').user == 'Paul'


def test_db_persistence():
    '''
    This test is a simple test of the DB, not important since the DB code and this test will need to get rewritten.
    '''
    from . import tube, db
    from .data import tension, leak
    tubes = db.db()
    dbman = db.db_manager(testing=True)
    dbman.wipe('confirm')
    tube1 = tube.Tube()
    tube2 = tube.Tube()
    tube1.set_ID("MSU0000001")
    tube2.set_ID("MSU0000001")
    tube1.tension.add_record(tension.TensionRecord(350))
    tube2.tension.add_record(tension.TensionRecord(355))
    tube2.leak.add_record(leak.LeakRecord(0))
    tubes.add_tube(tube1)
    tubes.add_tube(tube2)

    dbman.update(logging=False)

    del tubes
    tubes = db.db()

    tube4 = tubes.get_tube("MSU0000001")
    assert len(tube4.tension.get_record('all')) == 2
    assert tube4.leak.get_record('last').leak_rate == 0

    del tubes

    tubes = db.db()
    dbman.wipe('confirm')
    with pytest.raises(KeyError):
        tube4 = tubes.get_tube("MSU0000001")
    assert tubes.size() == 0


def test_db_add_tube():
    '''
    This test is a simple test of adding tubes to the DB, not important since the DB code and this test will need to get rewritten.
    '''
    from . import tube, db
    from .data import swage, tension, leak, dark_current
    tubes = db.db()
    dbman = db.db_manager(testing=True)
    dbman.wipe('confirm')
    tube1 = tube.Tube()
    tube2 = tube.Tube()
    tube1.set_ID("MSU0000001")
    tube2.set_ID("MSU0000001")
    tube1.tension.add_record(tension.TensionRecord(350))
    tube2.tension.add_record(tension.TensionRecord(355))
    tube2.leak.add_record(leak.LeakRecord(0))
    tubes.add_tube(tube1)
    dbman.update(logging=False)
    tube3 = tubes.get_tube("MSU0000001")
    assert len(tube3.tension.get_record('all')) == 1
    with pytest.raises(IndexError):
        tube3.leak.get_record('last').leak_rate == 0
    tubes.add_tube(tube2)
    dbman.update(logging=False)

    tube4 = tubes.get_tube("MSU0000001")
    assert len(tube4.tension.get_record('all')) == 2
    assert tube4.leak.get_record('last').leak_rate == 0


def test_tube_fail():
    from .tube import Tube
    from .data import leak
    tube1 = Tube()
    assert not tube1.fail()
    tube1.comment_fail = True
    assert tube1.fail()

    tube2 = Tube()
    tube2.leak.add_record(leak.LeakRecord(leak_rate=5))
    assert tube2.fail()


def test_tube_status():
    from .tube import Tube
    from .data.status import Status
    from .data import leak, swage, dark_current, tension
    import datetime

    tube1 = Tube()
    assert tube1.status() == Status.INCOMPLETE
    tube1.comment_fail = True
    assert tube1.status() == Status.FAIL
    tube1.comment_fail = True
    tube1.leak.add_record(leak.LeakRecord(leak_rate=5))
    assert tube1.status() == Status.FAIL

    tube2 = Tube()
    tube2.leak.add_record(leak.LeakRecord(leak_rate=0))
    assert tube2.status() == Status.INCOMPLETE
    tube2.dark_current.add_record(dark_current.DarkCurrentRecord(dark_current=0))
    assert tube2.status() == Status.INCOMPLETE
    tube2.swage.add_record(swage.SwageRecord(raw_length=-9.81, swage_length=0.07))
    assert tube2.status() == Status.INCOMPLETE
    tube2.tension.add_record(tension.TensionRecord(tension=350, date=datetime.datetime.now()))
    assert tube2.status() == Status.PASS
    tube2.tension.add_record(tension.TensionRecord(tension=350, date=datetime.datetime.now()-datetime.timedelta(days=15)))
    assert tube2.status() == Status.PASS

def test_locks():
    from .locks import Lock
    Lock.cleanup()
    lock = Lock("testing")
    assert not lock.is_locked()
    lock.lock()
    assert lock.is_locked()
    lock2 = Lock("testing")
    assert lock2.is_locked()
    lock.unlock()
    assert not lock.is_locked()
    assert not lock2.is_locked()
    lock2.lock()
    lock3 = Lock("testing2")
    assert not lock3.is_locked()
    assert lock.is_locked()
    del lock2
    assert not lock.is_locked()

def test_tube_str():
    from .tube import Tube
    tube1 = Tube()
    str(tube1)
