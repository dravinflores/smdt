###############################################################################
#   File: station.py
#   Author(s): Dravin Flores, Paul Johnecheck
#   Date Created: 02 April, 2021
#
#   Purpose: This file houses the base class that all station classes will
#       inherit from.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################

modes = {
    "last"  :  lambda station: station.m_records[-1],
    "first" :  lambda station: station.m_records[0],
    "all"   :  lambda station: station.m_records
    
}



class Station:
    """
    Abstract class representing a station that will record data on a tube
    """
    def __init__(self):
        # WARNING
        # Initially, this init function and the inheriting station's functions
        # looked something like
        # def __init__(self, records=[])
        #   self.m_records = records
        # I don't know why, but this is apparently a terrible idea
        # that somehow makes the lists in every station object be the same
        # object and share their users and records. Again, no idea why, I
        # encountered the problem and traced it back here and found that
        # removing it fixed it
        self.m_records = []


    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        ret = type(self)()
        ret.m_records = self.m_records + other.m_records
        return ret

    def fail(self):
        raise NotImplementedError

    def get_record(self, mode='last'):
        """Given a selected mode, returns the respective record"""
        if type(mode) == str:
            return modes[mode](self)
        elif type(mode) == type(lambda x: x): #Annoying but necessary hack to check if it's a lambda.
            return mode(self)
        else:
            raise RuntimeError()

    def add_record(self, record):
        """Adds a record to the station's records"""
        self.m_records.append(record)

    def visited(self):
        return len(self.m_records) != 0

    def status(self):
        raise NotImplementedError

