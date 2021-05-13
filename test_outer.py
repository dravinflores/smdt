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

def test_outer_swage():
    from sMDT.data import swage
    swage_station = swage.Swage()                                                #instantiate swage station object
    swage_station.add_record(swage.SwageRecord(raw_length=3.4, swage_length=3.2))#add 3 SwageRecords to the swage station
    swage_station.add_record(swage.SwageRecord(raw_length=5.2, swage_length=8))
    swage_station.add_record(swage.SwageRecord(raw_length=1.03, swage_length=5))
    print(swage_station.get_record("first"))                                     #print the first SwageRecord
    print(swage_station.fail("last"))                                            #print wether the tube fails based on the last record.


def test_outer_tension():
    from sMDT.data import tension
    tension_station = tension.Tension()                                                #instantiate tension station object
    tension_station.add_record(tension.TensionRecord(tension=350, frequency=3.2)) #add 3 TensionRecords to the tension station, nonsense values for frequency
    tension_station.add_record(tension.TensionRecord(tension=345, frequency=8))
    tension_station.add_record(tension.TensionRecord(tension=370, frequency=5))
    print(tension_station.get_record("first"))
    print(tension_station.fail("last"))                   #print the first TensionRecord, and whether the tube fails based on the last record.

def test_outer_leak():
    from sMDT.data import leak
    leak_station = leak.Leak()                                                #instantiate leak station object
    leak_station.add_record(leak.LeakRecord(leak_rate=0)) #add 3 LeakRecords to the leak station, nonsense values for frequency
    leak_station.add_record(leak.LeakRecord(leak_rate=5))
    leak_station.add_record(leak.LeakRecord(leak_rate=0.00000000001))
    print(leak_station.get_record("first"))
    print(leak_station.fail("last"))                   #print the first LeakRecord, and whether the tube fails based on the last record.

def test_outer_darkcurrent():
    from sMDT.data import dark_current
    darkcurrent_station = dark_current.DarkCurrent()                                                #instantiate darkcurrent station object
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(3)) #add 3 DarkCurrentRecords to the darkcurrent station, nonsense values for frequency
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(1e-10))
    darkcurrent_station.add_record(dark_current.DarkCurrentRecord(0))
    print(darkcurrent_station.get_record("first"))
    print(darkcurrent_station.fail("last"))                   #print the first DarkCurrentRecord, and whether the tube fails based on the last record.


if __name__ == '__main__':
    test_outer_darkcurrent()