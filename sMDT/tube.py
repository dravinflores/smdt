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
from .data.status import Status


class Tube:
    def __init__(self):
        self.m_tube_id = None
        self.m_comments = []
        self.swage = Swage()
        self.tension = Tension()
        self.leak = Leak()
        self.dark_current = DarkCurrent()
        self.legacy_data = dict()

    def __add__(self, other):
        ret = Tube()
        ret.m_tube_id = self.m_tube_id
        ret.m_comments = self.m_comments + other.m_comments
        ret.swage = self.swage + other.swage
        ret.leak = self.leak + other.leak
        ret.dark_current = self.dark_current + other.dark_current
        ret.tension = self.tension + other.tension
        ret.legacy_data = dict(self.legacy_data, **other.legacy_data)
        return ret

    def __str__(self):
        ret_str = ""
        ret_str += self.getID() + '\n'
        if len(self.m_comments) != 0:
            ret_str += "\nComments:\n"
        for comment in self.m_comments:
            ret_str += comment + '\n'
        else:
            ret_str += '\n'
        ret_str += self.swage.__str__()
        ret_str += self.tension.__str__()
        ret_str += self.leak.__str__()
        ret_str += self.dark_current.__str__()

        return ret_str

    def getID(self):
        return self.m_tube_id

    def get_comments(self):
        return self.m_comments

    def new_comment(self, comment: str):
        self.m_comments.append(comment)

    def fail(self):
        return any([x.fail() for x in [self.swage,self.leak,self.tension,self.dark_current]])

    def status(self):
        stations = [self.swage, self.tension, self.leak, self.dark_current]
        if any([i.status() == Status.FAIL for i in stations]):
            return Status.FAIL
        elif any([i.status() == Status.INCOMPLETE for i in stations]):
            return Status.INCOMPLETE
        elif all([i.status() == Status.PASS for i in stations]):
            return Status.PASS
        else:
            raise RuntimeError #this should be impossible if the station status are implemented correctly


if __name__ == '__main__':
    a = Tube()
    print(a)
