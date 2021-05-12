#testing how the outer library access works.

def test_outer():
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
    from sMDT import tube
    from sMDT.data import station,tension
    tube1 = tube.Tube()
    tube1.tension.add_record(tension.TensionRecord(350))
    tube1.tension.add_record(tension.TensionRecord(370))
    tube1.tension.add_record(tension.TensionRecord(330))
    assert tube1.tension.get_record(highest).tension == 370

def test_outer_modes():
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
    assert not t.fail(mode='first')
    assert t.fail(lambda x: max(x.m_records, key=lambda y: y.tension))

if __name__ == '__main__':
    test_outer_modes()