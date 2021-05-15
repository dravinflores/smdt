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
    import tube
    from data import swage,tension,leak,dark_current
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
    import tube
    tube1 = tube.Tube()
    tube1.new_comment("This tube is for testing purposes")
    assert tube1.get_comments() == ["This tube is for testing purposes"]

def test_tube_add():
    '''
    This tests the __add__ override that tubes support.
    '''
    import tube
    from data import swage,tension,leak,dark_current
    tube1 = tube.Tube()
    tube2 = tube.Tube()
    tube1.m_tube_id = "MSU0000001"
    tube2.m_tube_id = "MSU0000001"
    tube1.tension.add_record(tension.TensionRecord(350))
    tube2.tension.add_record(tension.TensionRecord(355))
    tube2.leak.add_record(leak.LeakRecord(0))
    tube3 = tube1 + tube2
    print(tube3.tension.get_record('all'))
    assert len(tube3.tension.get_record('all')) == 2
    assert tube3.leak.get_record('last').leak_rate == 0

def test_db_persistence():
    '''
    This test is a simple test of the DB, not important since the DB code and this test will need to get rewritten.
    '''
    import tube,db
    from data import tension,leak
    tubes = db.db()
    dbman = db.db_manager()
    dbman.wipe()
    tube1 = tube.Tube()
    tube2 = tube.Tube()
    tube1.m_tube_id = "MSU0000001"
    tube2.m_tube_id = "MSU0000001"
    tube1.tension.add_record(tension.TensionRecord(350))
    tube2.tension.add_record(tension.TensionRecord(355))
    tube2.leak.add_record(leak.LeakRecord(0))
    tubes.add_tube(tube1)
    tubes.add_tube(tube2)

    dbman.update()

    del tubes
    tubes = db.db()

    tube4 = tubes.get_tube("MSU0000001")
    assert len(tube4.tension.get_record('all')) == 2
    assert tube4.leak.get_record('last').leak_rate == 0

    del tubes

    tubes = db.db()
    dbman.wipe()
    with pytest.raises(KeyError):
        tube4 = tubes.get_tube("MSU0000001")
    assert tubes.size() == 0



def test_db_add_tube():
    '''
    This test is a simple test of adding tubes to the DB, not important since the DB code and this test will need to get rewritten.
    '''
    import tube, db
    from data import swage,tension,leak,dark_current
    tubes = db.db()
    dbman = db.db_manager()
    dbman.wipe()
    tube1 = tube.Tube()
    tube2 = tube.Tube()
    tube1.m_tube_id = "MSU0000001"
    tube2.m_tube_id = "MSU0000001"
    tube1.tension.add_record(tension.TensionRecord(350))
    tube2.tension.add_record(tension.TensionRecord(355))
    tube2.leak.add_record(leak.LeakRecord(0))
    tubes.add_tube(tube1)
    dbman.update()
    tube3 = tubes.get_tube("MSU0000001")
    assert len(tube3.tension.get_record('all')) == 1
    with pytest.raises(IndexError):
        tube3.leak.get_record('last').leak_rate == 0
    tubes.add_tube(tube2)
    dbman.update()

    tube4 = tubes.get_tube("MSU0000001")
    assert len(tube4.tension.get_record('all')) == 2
    assert tube4.leak.get_record('last').leak_rate == 0

if __name__ == "__main__":
    test_db_add_tube()
