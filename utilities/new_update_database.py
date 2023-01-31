###############################################################################
#   File: new_update_database.py
#   Author(s): Sara Sawford
#   Date Created: 30 January, 2023
#
#   Purpose: This program reads in the CSV file from UMich and adds
#       UMich data to existing tube or creates new tube and adds
#       data
#
#   Known Issues:
#
#   Workarounds:
#
#   Updates:
#
###############################################################################


import pandas as pd
import time
import datetime

from sMDT.tube import Tube
from sMDT import db

from sMDT.data.swage import SwageRecord
from sMDT.data.tension import TensionRecord
from sMDT.data.dark_current import DarkCurrentRecord
from sMDT.data.bent import BentRecord
from sMDT.data.leak import LeakRecord
from sMDT.data.umich import UMich_BentRecord, UMich_DarkCurrentRecord, UMich_MiscRecord, UMich_TensionRecord


umich= pd.read_csv("UMTUBE2MSU.csv" ,delimiter=",")


database = db.db()


# Adding University of Michigan records from the CSV file to the tube object
# tube- object created by New_Tube
# row- the row of which the tube's barcode can be found in the csv file
# Returns tube object with attributes defined from the UMich csv 
def umich_tube_records(tube, row):

        # Adding UMich Tension Records
        umich_tension = umich.loc[row]['LastTension[g]'].tolist()[0]
        umich_frequency = umich.loc[row]['LastFrequency[Hz]'].tolist()[0]
        umich_date = umich.loc[row]['LastTensionDate'].tolist()[0]
        umich_tension_flag = umich.loc[row]['Tensionflag'].tolist()[0]
        umich_freq_diff = umich.loc[row]['FreqDiff[Hz]'].tolist()[0]
        umich_tens_diff = umich.loc[row]['TensDiff[g]'].tolist()[0]
        umich_time_diff = umich.loc[row]['TimeDiff[D]'].tolist()[0]
        umich_flg_scd = umich.loc[row]['flag2ndTension'].tolist()[0]


        # Make sure umich_date and umich_tension are in correct format for the DatabaseViewer
        if isinstance(umich_date, (str)):
                umich_date = datetime.datetime.strptime(umich_date, '%y-%m-%d')

        else:
                try:
                        umich_date = str(umich_date)
                except:
                        umich_date = umich_date

        if isinstance(umich_tension, (float, int)):
                pass
        else:
                umich_tension = None

       
        tube.umich_tension.add_record(UMich_TensionRecord(umich_tension=umich_tension,
                                                        umich_frequency=umich_frequency,
                                                        umich_date=umich_date,
                                                        tension_flag=umich_tension_flag,
                                                        freq_diff = umich_freq_diff,
                                                        tens_diff = umich_tens_diff,
                                                        time_diff = umich_time_diff,
                                                        flag_scd_tension = umich_flg_scd))

        
        # Adding UMich Bent Records
        umich_bent = umich.loc[row]['bent[mm]'].tolist()[0]

        tube.umich_bent.add_record(UMich_BentRecord(umich_bent=umich_bent))


        # Adding UMich Dark Current Records
        umich_dc = umich.loc[row]['DC[nA]'].tolist()[0]
        umich_dc_date = umich.loc[row]['DCday'].tolist()[0]
        umich_dc_flag = umich.loc[row]['DCflag'].tolist()[0]
        umich_hv = umich.loc[row]['HVtime[s]'].tolist()[0]

        if isinstance(umich_dc_date, (str)):
                umich_dc_date = datetime.datetime.strptime(umich_dc_date, '%y-%m-%d')
        else:
                umich_dc_date = umich_dc_date


        tube.umich_dark_current.add_record(UMich_DarkCurrentRecord(umich_dark_current=umich_dc,
                                                                umich_date=umich_dc_date,
                                                                dc_flag=umich_dc_flag,
                                                                hv_time=umich_hv))


        # Adding Miscellaneous Data
        prod_site = umich.loc[row]['ProdSite'].tolist()[0]      
        endplug_type = umich.loc[row]['endplugType'].tolist()[0]
        first_scan = umich.loc[row]['1stScan'].tolist()[0]
        flag_endplug = umich.loc[row]['flagEndplug'].tolist()[0]
        length = umich.loc[row]['Length[mm]'].tolist()[0]
        done = umich.loc[row]['done?'].tolist()[0]

        if isinstance(first_scan, (str)):
                first_scan = datetime.datetime.strptime(first_scan, '%Y-%m-%d')
        else:
                first_scan = first_scan 


        tube.umich_misc.add_record(UMich_MiscRecord(prod_site = prod_site,
                                                endplug_type = endplug_type,
                                                first_scan = first_scan,
                                                flag_endplug = flag_endplug,
                                                length = length,
                                                done = done))

        return(tube)


#### Start of main program ####


# tube_dict = old_database.open_shelve()
tube_dict = database.open_shelve()


# Create list of all barcodes in UMich csv
# If a barcode is in MSU database but not this list, then UMich hasn't received that tube OR UMich produced it
lst = umich['tubeID'].tolist()

print("Looping over ",len(tube_dict)," tubes in current database")
#print(lst)
#return 0

counter=0

for barcode in tube_dict:
        # Find tube currently in db
        tube = tube_dict[barcode]
        counter += 1
        # update and maybe sleep every 1000 tubes to give the manager time to keep up
        if counter%1000 == 0:
                print("Processing tube ",counter," , ID ",barcode)
                time.sleep(5)

        # Checks if the MSU barcode is in the UMich list of barcodes
        # If not in list, don't create UMich records for the tube
        if barcode in lst:
                row = umich.index[(umich['tubeID'] == barcode).tolist()]
                #print("adding UMich info for tube ",barcode)
                tube = umich_tube_records(tube, row)
        # Adds tube with MSU records (and UMich records if they exist)
        database.overwrite_tube(tube)


print("Cross-check: number of tubes in new database: ",database.size())
time.sleep(5)
print("Cross-check: number of tubes in new database: ",database.size())

        
# List of barcodes that are in UMich barcode list, but not MSU database
# We don't have test information from MSU because UMich made them
umich_barcodes = list(set(lst) - set(tube_dict))
print("Number of tubes made at UMich since last update: ",len(umich_barcodes))

counter=0
for barcode in umich_barcodes:
        # print(barcode)
        tube = Tube()
        tube.set_ID(barcode)
        counter += 1
        # sleep every 1000 tubes to give the manager time to keep up
        if counter%1000 == 0:
                print("Processing tube ",counter," , ID ",barcode)
                #time.sleep(3)
        
        row = umich.index[(umich['tubeID'] == barcode).tolist()]
        tube = umich_tube_records(tube, row)
        # print(tube)

        # Adds tube with only UMich records
        database.overwrite_tube(tube)

print("Finished! Now you have to wait for the manager to add all of the tubes")


database.close_shelve(tube_dict)


