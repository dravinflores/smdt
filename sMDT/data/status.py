###############################################################################
#   File: status.py
#   Author(s): Dravin Flores, Paul Johnecheck, Sara Sawford
#   Status code for sMDT tubes
#

from enum import IntEnum

class Status(IntEnum):
    FAIL = 0
    PASS = 2
    INCOMPLETE = 1

class UMich_Status(IntEnum):
    UMICH_COMPLETE = 3
    UMICH_INCOMPLETE = 4
    NO_DATA = 5
    PASS = 6
    FAIL = 7

class ErrorCodes(IntEnum):
    NO_ERROR = 0
    ERROR_DESCRIBED_IN_COMMENT = 1
    SWAGED_IMPROPERLY = 2
    WIRE_SNAPPED = 3
    DAMAGED_WIRE_COULDNT_TENSION = 4
    WIRE_LOST_IN_SWAGED_TUBE = 5
    FERRULE_BUMPED_AFTER_TENSIONING = 6
    SHIM_FITS_0_8MM = 7
    SHIM_FITS_1_6MM = 8
    SHIM_FITS_2_4MM = 9
