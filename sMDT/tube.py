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
        self.comment_fail = False # Depricated

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
            ret_str += self.get_ID() + '-' + self.status().name + '\n'
        if len(self.m_comments) != 0:
            ret_str += "\nComments:\n"
        for comment, user, date, error_code in self.m_comments:
            ret_str += comment + " -" + user + " " + date.date().isoformat() + " " + error_code.name + '\n\n'
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

    def set_ID(self, ID):
        self.m_tube_id = ID

    def get_comments(self):
        return self.m_comments

    def new_comment(self, comment: str):
        self.m_comments.append(comment)

    def fail(self):
        return self.status() == Status.FAIL

    def comment_fails(self):
        ok_error_codes = [ErrorCodes.NO_ERROR, 
                          ErrorCodes.SHIM_FITS_2_4MM, 
                          ErrorCodes.SHIM_FITS_1_6MM, 
                          ErrorCodes.SHIM_FITS_0_8MM]
        for comment in self.m_comments:
            if comment[3] not in ok_error_codes:
                return True
        return False

    def status(self):
        stations = [self.swage, self.tension, self.leak, self.dark_current]
        if any([i.status() == Status.FAIL for i in stations]) or self.comment_fails():
            return Status.FAIL
        elif any([i.status() == Status.INCOMPLETE for i in stations]):
            return Status.INCOMPLETE
        elif all([i.status() == Status.PASS for i in stations]):
            return Status.PASS
        else:
            raise RuntimeError  # this should be impossible if the station status are properly mutually exclusive
