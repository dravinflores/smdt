#testing how the outer library access works.

def test_outer():
    from sMDT import db,tube
    from sMDT.data import tension
    tubes = db.db()
    tube1 = tube.Tube()
    tube1.tension.add_record(tension.TensionRecord(1.5))
    assert tube1.tension.get_record().tension == 1.5

if __name__ == '__main__':
    test_outer()