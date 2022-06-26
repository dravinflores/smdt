###############################################################################
#   File: tube.py
#   Author(s): Sara Sawford
#   Date Created: 24 June, 2022
#
#   Purpose: This is the class representing any data from University of Michigan
#   CSV files.
#
#   Known Issues:
#
#   Workarounds:
#
###############################################################################



import os
import textwrap
from abc import ABC
from .station import Station
from .record import Record


from sMDT.data.tension import Tension,TensionRecord
from sMDT.data.bent import Bent, BentRecord
from sMDT.data.dark_current import DarkCurrent, DarkCurrentRecord
from sMDT.data.status import UMich_Status



class UMich_BentRecord(BentRecord):
    """
    Class for objects representing individual records from University of 
    Michigan's bentness tests. These are bentness tests after a tube is produced
    """
    # Only one column in the UMich csv file seems relevant to our Bentness Station
    def __init__(self,
                umich_bent = None
    ):
            # Calling super class init to contruct the object
            super().__init__()
            self.umich_bent = umich_bent 


    def __str__(self):
        a = f"UMich bentness: {self.umich_bent}\n\n" 
        return a



class UMich_Bent(Bent):
    """"
    UMich Bent Class, to manage relevent records for a particular tube
    """

    # Created using metaclass because UMich_Status as a parent class caused issues
    __metaclass__ = UMich_Status

    def __init__(self): 
         super().__init__()

    def __str__(self):
        a = "UMich Bentness Data: " + (self.status().name or '') + "\n"
        b = ""
        
        # Iterates through each record per tube
        if self.status() == UMich_Status.UMICH_COMPLETE or self.status() == UMich_Status.UMICH_INCOMPLETE:
            for record in sorted(
                    # Checks that the bentness is a float; if not, either n/a or 0 in the csv file
                    self.m_records, key=lambda i: (i.umich_bent is float, i.umich_bent)
            ):
                b += record.__str__()

            b = b[:-1]

        else:
            pass
        return a + textwrap.indent(b, '\t') + '\n'
            
            
    def status(self):

        # If there are no UMich records for the tube, set status to NO_DATA
        record = None

        try:
            record = self.get_record().umich_bent
        except:
            pass

        if isinstance(record, float):
            return UMich_Status.UMICH_COMPLETE
        if isinstance(record, (int, str)):
            return UMich_Status.UMICH_INCOMPLETE
        else:
            return UMich_Status.NO_DATA

       

class UMich_TensionRecord(TensionRecord):
    """
    Class for objects representing individual records from University of 
    Michigan's tension tests
    """

    def __init__(self,
                umich_tension = None,
                umich_frequency = None,
                umich_date = None,
                tension_flag = None,
                freq_diff = None,
                tens_diff = None,
                time_diff = None,
                flag_scd_tension = None
    ):

        # Calling super class to construct the object
        super().__init__()
        self.umich_tension = umich_tension
        self.umich_frequency = umich_frequency
        self.umich_date = umich_date
        self.tension_flag = tension_flag
        self.freq_diff = freq_diff
        self.tens_diff = tens_diff
        self.time_diff = time_diff
        self.flag_scd_tension = flag_scd_tension



    def __str__(self):
        # Using string concatenation as return string
        a = f"Tension: {self.umich_tension}\n"
        b = f"Frequency: {self.umich_frequency}\n"
        c = f"First Tension Flag: {self.tension_flag}\n"
        d = f"Frequency Difference: {self.freq_diff}\n"
        e = f"Tension Difference: {self.tens_diff}\n"
        f = f"Time Difference: {self.time_diff}\n"
        g = f"Second Tension Flag: {self.flag_scd_tension}\n"
        h = f"Recorded on: {self.umich_date}\n\n"


        return_str = a + b + c + d + e + f + g + h
        return return_str



class UMich_Tension(Tension):
    """
    UMich Tension class, manages the relevant records for a particular tube.
    """

    # Used metaclass because inheritance from UMich_Status resulted in errors
    __metaclass__ = UMich_Status

    def __init__(self): 
         super().__init__()

    def __str__(self):
        a = "UMich Tension Data: " + (self.status().name or '') + "\n"
        b = ""
        
        # We want to print out each record.
        if self.status() == UMich_Status.FAIL or self.status() == UMich_Status.PASS:
            for record in sorted(
                    # If the tube does not exists in the UMich csv, i.flag_scd_tension will be None
                    # If the tube exists, flag_scd_tension will be a string
                    self.m_records, key=lambda i: (i.flag_scd_tension is not None, i.flag_scd_tension)
            ):
                b += record.__str__()

            b = b[:-1]

        else:
            pass
        return a + textwrap.indent(b, '\t') + '\n'
            
            
    def status(self):

        # If the tube does not exist in the csv, the record will stay None
        record = None

        try:
            record = self.get_record().flag_scd_tension
        except:
            pass

        # Checks if the tube passed or failed the tension tests, or doesn't exist
        if record == 'Fail2*' or record == 'Fail2':
            return UMich_Status.FAIL
        elif record == 'Pass2' or record == 'Pass2*':
            return UMich_Status.PASS
        elif record == None:
            return UMich_Status.NO_DATA
        else:
            return UMich_Status.UMICH_INCOMPLETE

            





class UMich_DarkCurrentRecord(DarkCurrentRecord):
    """
    Class for objects representing individual records from University of 
    Michigan's dark current tests
    """

    def __init__(self,
                umich_dark_current = None,
                umich_date = None,
                dc_flag = None,
                hv_time = None
    ):
        super().__init__()
        self.umich_dark_current = umich_dark_current
        self.umich_date = umich_date
        self.dc_flag = dc_flag
        self.hv_time = hv_time

    def __str__(self):

        # Using string concatination for return value
        a = f"Dark Current: {self.umich_dark_current}\n"
        b = f"Dark Current Flag: {self.dc_flag}\n"
        c = f"HV Time[s]: {self.hv_time}\n"
        d = f"Recorded on: {self.umich_date}\n\n"

        return_str = a + b + c + d
        return return_str



class UMich_DarkCurrent(DarkCurrent):
    """
    UMich Tension class, manages the relevant records for a particular tube.
    """
    # Used metaclass because inheritance from UMich_Status resulted in errors
    __metaclass__ = UMich_Status

    def __init__(self): 
         super().__init__()

    def __str__(self):
        a = "UMich Dark Current Data: " + (self.status().name or '') + "\n"
        b = ""
        
        # We want to print out each record.
        if self.status() == UMich_Status.PASS or self.status() == UMich_Status.FAIL:
            for record in sorted(
                    self.m_records, key=lambda i: (i.dc_flag is not None, i.dc_flag)
            ):
                b += record.__str__()

            b = b[:-1]

            # We want to have the return string indent each record, for 
            # viewing ease.
        else:
            pass
        return a + textwrap.indent(b, '\t') + '\n'
            
            
    def status(self):

        record = None

        try:
            record = self.get_record().dc_flag
        except:
            pass

        if record == 'OK':
            return UMich_Status.PASS
        elif record == 'BAD' or record == 'WARN':
            return UMich_Status.FAIL
        elif record == None:
            return UMich_Status.NO_DATA
        else:
            return UMich_Status.UMICH_INCOMPLETE



class UMich_MiscRecord(Record):
    """
    Class for objects representing individual records not involved in the 
    bentness, tension, or dark current testing from University of Michigan
    """

    def __init__(self,
                prod_site = None,
                endplug_type = None,
                first_scan = None,
                flag_endplug = None,
                length = None,
                done = None
    ):
        self.prod_site = prod_site
        self.endplug_type = endplug_type
        self.first_scan = first_scan
        self.flag_endplug = flag_endplug
        self.length = length
        self.done = done

    def __str__(self):
        a = f"Production Site: {self.prod_site}\n"
        b = f"Endplug Type: {self.endplug_type}\n"
        c = f"Endplug Flag: {self.flag_endplug}\n"
        d = f"1st Scan: {self.first_scan}\n"
        e = f"Tube Length: {self.length}\n"
        f = f"Done? : {self.done}\n"
        
        return_str = a + b + c + d + e + f
        return return_str


class UMich_Misc(Station, ABC):
    """
    UMich Miscellaneous class, manages the relevant records for a particular tube.
    """

    __metaclass__ = UMich_Status

    def __init__(self): 
         super().__init__()

    def __str__(self):
        a = "UMich Misc Data: " + (self.status().name or '') + "\n"
        b = ""
        

        if self.status() == UMich_Status.PASS or self.status() == UMich_Status.UMICH_INCOMPLETE:
            for record in sorted(
                    # i.done is either 'yes', 'no', or NoneType
                    self.m_records, key=lambda i: (i.done is str, i.done)
            ):
                b += record.__str__()

            b = b[:-1]

        else:
            pass
        return a + textwrap.indent(b, '\t') + '\n'
            
            
    def status(self):

        record = None

        # Using the 'done?' column to determine status of entire tube
        try:
            record = self.get_record().done
        except:
            pass
        if record == 'yes':
            return UMich_Status.PASS
        elif record == 'no':
            return UMich_Status.UMICH_INCOMPLETE
        elif record == None:
            return UMich_Status.NO_DATA
