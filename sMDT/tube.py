###############################################################################
#   File: tube.py
#   Author(s): Paul Johnecheck, Dravin Flores
#   Date Created: 16 April, 2021
#
#   Purpose: This is the class representing a tube.
#    an application will create these and store them in the database
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################


from .data.swage import Swage
from .data.tension import Tension
from .data.leak import Leak
from .data.dark_current import DarkCurrent
from .data.status import Status, ErrorCodes
from .data.bent import Bent


class Tube:
    def __init__(self):
        self.m_tube_id = None
        self.m_comments = []
        self.swage = Swage()
        self.tension = Tension()
        self.leak = Leak()
        self.dark_current = DarkCurrent()
        self.legacy_data = dict()
        self.bent = Bent()
        self.comment_fail = False

    def __add__(self, other):
        ret = Tube()
        ret.m_tube_id = self.m_tube_id
        ret.m_comments = self.m_comments + other.m_comments
        ret.swage = self.swage + other.swage
        ret.leak = self.leak + other.leak
        ret.dark_current = self.dark_current + other.dark_current
        ret.tension = self.tension + other.tension
        ret.bent = self.bent + other.bent
        ret.legacy_data = dict(self.legacy_data, **other.legacy_data)
        return ret

    def __str__(self):
        ret_str = ""
        if self.get_ID():
            ret_str += self.get_ID() + '-' + (self.status().name or '') + '\n'
        date_str=self.get_mfg_date()
        if date_str != None:
            ret_str += 'Manufacture date ' +str(date_str) + '\n'
        else:
            ret_str += 'No information on manufacture date\n'
        if len(self.m_comments) != 0:
            ret_str += "\nComments:\n"
        for comment, user, date, error_code in self.m_comments:
            ret_str += (comment or '') \
                       + " -" \
                       + (user or '') \
                       + " " \
                       + (date.date().isoformat() if date is not None else '') \
                       + " " \
                       + (error_code.name or '') \
                       + '\n\n'

        if any([code != 0 for (h, e, y, code) in self.m_comments]):
            ret_str = ret_str[:-1]
            ret_str += "\nMARKED AS FAIL BY COMMENT\n\n"
        ret_str += self.swage.__str__()
        ret_str += self.tension.__str__()
        ret_str += self.leak.__str__()
        ret_str += self.bent.__str__()
        ret_str += self.dark_current.__str__()

        return ret_str

    def get_ID(self):
        return self.m_tube_id

    def set_ID(self, barcode):
        proper_length = len("MSU00123")
        extra_character_index = proper_length
        self.m_tube_id = barcode.strip()      

    def get_comments(self):
        return self.m_comments

    def new_comment(self, comment: str):
        self.m_comments.append(comment)

    def fail(self):
        return self.status() == Status.FAIL

    def comment_fails(self):
        ok_error_codes = [
            ErrorCodes.NO_ERROR,
            ErrorCodes.SHIM_FITS_2_4MM,
            ErrorCodes.SHIM_FITS_1_6MM,
            ErrorCodes.SHIM_FITS_0_8MM
        ]

        for comment in self.m_comments:
            if comment is not None and len(comment) > 3:
                if comment[3] not in ok_error_codes:
                    return True
        return False

    def status(self):
        stations = [self.swage, self.tension, self.leak, self.dark_current]

        if self.swage is None \
                or self.tension is None \
                or self.leak is None \
                or self.dark_current is None:
            return Status.INCOMPLETE
        
        if self.status_bentness() == Status.FAIL: return Status.FAIL

        if any([i.status() == Status.FAIL for i in stations if i is not None]) \
                or self.comment_fails() \
                or self.comment_fail:
            return Status.FAIL
        elif any([
            i.status() == Status.INCOMPLETE for i in stations if i is not None
        ]):
            return Status.INCOMPLETE
        elif all([
            i.status() == Status.PASS for i in stations if i is not None
        ]):
            return Status.PASS
        else:
            # this should be impossible if the station status
            # are properly mutually exclusive
            raise RuntimeError

    def status_bentness(self):
        # special case accounting: if bent is 0.8, then this is pass for some but fail for others
        # in that case, check if swage is incomplete, if so then mark as fail, otherwise mark bent as
        # pass
        if not self.bent.visited(): return Status.PASS
        if self.bent.status()==Status.INCOMPLETE and self.swage is not None: return Status.PASS
        if self.bent.bentness()==0.8 and self.swage is None: return Status.FAIL
        if self.bent.bentness()==0.8 and self.swage.status() == Status.INCOMPLETE: return Status.FAIL
        return self.bent.status()
            
        
        
    def to_dict(self):
        tube_in_dict = dict()
        swager_station = dict()
        tension_station = dict()
        leak_station = dict()
        dark_current_station = dict()
        bentness_station = dict()

        swager_station['m_records'] = []
        tension_station['m_records'] = []
        leak_station['m_records'] = []
        dark_current_station['m_records'] = []
        bentness_station['m_records'] = []

        for record in self.swage.get_record('all'):
            record_dict = dict()
            record_dict['raw_length'] = record.raw_length
            record_dict['swage_length'] = record.swage_length
            record_dict['clean_code'] = record.clean_code
            record_dict['date'] = record.date
            record_dict['user'] = record.user
            swager_station['m_records'].append(record_dict)

        for record in self.tension.get_record('all'):
            record_dict = dict()
            record_dict["tension"] = record.tension,
            record_dict["frequency"] = record.frequency,
            record_dict["date"] = record.date,
            record_dict["user"] = record.user
            tension_station['m_records'].append(record_dict)
            
        for record in self.leak.get_record('all'):
            record_dict = dict()
            record_dict["leak_rate"] = record.leak_rate
            record_dict["date"] = record.date
            record_dict["user"] = record.user
            leak_station['m_records'].append(record_dict)
            
        for record in self.dark_current.get_record('all'):
            record_dict = dict()
            record_dict["dark_current"] = record.dark_current
            record_dict["date"] = record.date
            record_dict["voltage"] = record.voltage
            record_dict["user"] = record.user
            dark_current_station['m_records'].append(record_dict)

        for record in self.bent.get_record('all'):
            record_dict = dict()
            record_dict["bentness"] = record.bentness
            record_dict["date"] = record.date
            record_dict["user"] = record.user
            bentness_station['m_records'].append(record_dict)

        tube_data_dict = dict()

        tube_data_dict['swage_station'] = swager_station
        tube_data_dict['tension_station'] = tension_station
        tube_data_dict['leak_station'] = leak_station
        tube_data_dict['dark_current_station'] = dark_current_station

        tube_in_dict[self.m_tube_id] = tube_data_dict

        return tube_in_dict
    def get_mfg_date(self):
        swage_date=None
        try:
            for record in self.swage.m_records:
                swage_date = record.date
                if swage_date != None: return swage_date
        except IndexError:
            swage_date = None

        # swage record doesn't contain a date, check bent
        if swage_date == None:
            try:
                for record in self.bent.m_records:
                    swage_date = record.date
                    if swage_date != None: return swage_date
            except IndexError:
                swage_date = None
                
        # swage and bent record doesn't contain a date, check tension
        if swage_date == None:
            try:
                for record in self.tension.m_records:
                    swage_date = record.date
                    if swage_date != None: return swage_date
            except IndexError:
                swage_date = None

        # swage and bent and tension record doesn't contain a date, check dark_current
        if swage_date == None:
            try:
                for record in self.dark_current.m_records:
                    swage_date = record.date
                    if swage_date != None: return swage_date
            except IndexError:
                swage_date = None
            
        # station records doesn't contain a date, check comments
        if swage_date == None:
            if len(self.m_comments) != 0:
                for comment, user, date, error_code in self.m_comments:
                    swage_date=date
                    if swage_date != None: return swage_date
            #else:
            #print("Error getting any date for tube, "+self.get_ID())
                

        return swage_date
