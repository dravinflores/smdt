###############################################################################
#   File: test_tube_db.py
#   Author(s): Paul Johnecheck
#   Date Created: 02 April, 2021
#
#   Purpose: This file is the home of the test cases 
#   for the tube and the db classes.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

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
    assert len(tube3.tension.get_record('all')) == 2
    assert tube3.leak.get_record('last').leak_rate == 0

def test_db():
    '''
    This test is a simple test of the DB, not important since the DB code and this test will need to get rewritten.
    '''
    pass