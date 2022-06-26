###############################################################################
#   File: DatabaseViewer.py
#   Author(s): Sara Sawford
#   Date Created: 24 June, 2022
#
#   Purpose: This program reads in the CSV file from UMich and creates
#       a new Tube object to be added to the database
#
#   Known Issues:
#
#   Workarounds: Adding swage records to the new database caused errors unless 
#               NoneType records were removed
#
#   Updates:
#
###############################################################################


import pandas as pd
import time
import datetime

from sMDT.tube import Tube
from sMDT import db
from sMDT import db_legacy

from sMDT.data.swage import SwageRecord
from sMDT.data.tension import TensionRecord
from sMDT.data.dark_current import DarkCurrentRecord
from sMDT.data.bent import BentRecord
from sMDT.data.leak import LeakRecord
from sMDT.data.umich import UMich_BentRecord, UMich_DarkCurrentRecord, UMich_MiscRecord, UMich_TensionRecord


umich= pd.read_csv("umich.csv" ,delimiter=",")

# old_database does not contain UMich records
# database is the updated version to contain UMich records
old_database = db_legacy.db()
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

        tube.umich_misc.add_record(UMich_MiscRecord(prod_site = prod_site,
                                                endplug_type = endplug_type,
                                                first_scan = first_scan,
                                                flag_endplug = flag_endplug,
                                                length = length,
                                                done = done))

        return(tube)



# Gets records from MSU database and adds them to new database
# tube- new tube object
# old- old tube object from MSU database
# Returns tube with records from the old database
def msu_tube_records(tube, old):

        tube.m_comments = old.m_comments
        tube.legacy_data = old.legacy_data
        tube.comment_fail = old.comment_fail

        
        # Adding Tension Records

        tension_station = {}
        tension_station['m_records'] = []

        for record in old.tension.get_record('all'):
                record_dict = dict()
                record_dict["tension"] = record.tension
                record_dict["frequency"] = record.frequency
                record_dict["date"] = record.date
                record_dict["user"] = record.user
                tension_station['m_records'].append(record_dict)
            

        for record in tension_station['m_records']:
                        tube.tension.add_record(TensionRecord(tension=record['tension'],
                                                        frequency=record['frequency'],
                                                        date=record['date'],
                                                        user=record['user']))

        # Adding Swage Records
        
        swage = {}
        swage['m_records'] = []
        
        for record in old.swage.get_record('all'):
                record_dict = dict()
                record_dict['raw_length'] = record.raw_length
                record_dict['swage_length'] = record.swage_length
                record_dict['clean_code'] = record.clean_code
                record_dict['date'] = record.date
                record_dict['user'] = record.user
                swage['m_records'].append(record_dict)

        for record in swage['m_records']:
                # Included this if-statement because any NoneTypes seemed to interfere with the DatabaseViewer
                if record['raw_length'] == None:
                        pass
                else:
                        tube.swage.add_record(SwageRecord(raw_length=record['raw_length'],
                                                swage_length=record['swage_length'],
                                                clean_code=record['clean_code'],
                                                date=record['date'],
                                                user=record['user']))
                
        #Adding Bent Records

        bentness = {}
        bentness['m_records'] = []

        for record in old.bent.get_record('all'):
                record_dict = dict()
                record_dict['bent'] = record.bentness
                record_dict['date'] = record.date
                record_dict['user'] = record.user
                bentness['m_records'].append(record_dict)


        for record in bentness['m_records']:
                        tube.bent.add_record(BentRecord(bentness=record['bent'],
                                                        date=record['date'],
                                                        user=record['user']))


        # Adding Dark Current Records

        dc = {}
        dc['m_records'] = []

        for record in old.dark_current.get_record('all'):
                record_dict = dict()
                record_dict['dark_current'] = record.dark_current
                record_dict['date'] = record.date
                record_dict['voltage'] = record.voltage
                record_dict['user'] = record.user
                dc['m_records'].append(record_dict)


        for record in dc['m_records']:
                tube.dark_current.add_record(DarkCurrentRecord(dark_current=record['dark_current'],
                                                date=record['date'],
                                                voltage=record['voltage'],
                                                user=record['user']))  
        

        # Adding Leak Test Records
        leak_dict = {}
        leak_dict['m_records'] = []

        # Used this format of for loop because would not work when formated as
        # for record in old.leak.get_record('all'):
                # record_dict = dict()
                # record_dict['leak_rate'] = record.leak_rate
                # record_dict['date'] = record.date
                # record_dict['user'] = record.user
                # leak_dict['m_records'].append(record_dict)

        for i in range(len(old.leak.get_record('all'))):
                record_dict = dict()
                record_dict['leak_rate'] = old.leak.get_record('all')[i].leak_rate
                record_dict['date'] = old.leak.get_record('all')[i].date
                record_dict['user'] = old.leak.get_record('all')[i].user
                leak_dict['m_records'].append(record_dict)


        for record in leak_dict['m_records']:
                        tube.leak.add_record(LeakRecord(leak_rate=record['leak_rate'],
                                                        date=record['date'],
                                                        user=record['user']))
        return(tube)





 


#### Start of main program ####


tube_dict = old_database.open_shelve()


# Create list of all barcodes in UMich csv
# If a barcode is in MSU database but not this list, then UMich hasn't received that tube
lst = umich['tubeID'].tolist()

print("Copying ",len(tube_dict)," tubes from old to new database")

counter=0
for barcode in tube_dict:

        # Creating new tube object with UMich attributes
        tube = Tube()
        tube.set_ID(barcode)
        old = tube_dict[barcode]
        counter += 1
        # update and maybe sleep every 1000 tubes to give the manager time to keep up
        if counter%1000 == 0:
                print("Processing tube ",counter," , ID ",barcode)
                time.sleep(5)

        # Tube object has records from MSU database
        tube = msu_tube_records(tube, old)

        # Checks if the MSU barcode is in the UMich list of barcodes
        # If not in list, don't create UMich records for the tube
        if barcode in lst:
                row = umich.index[(umich['tubeID'] == barcode).tolist()]
                #tube = umich_tube_records(tube, row)
        else:
                pass   

        # Adds tube with MSU records (and UMich records if they exist)
        database.add_tube(tube)


print("Cross-check: number of tubes in new database: ",database.size())
time.sleep(5)
print("Cross-check: number of tubes in new database: ",database.size())

        
# List of barcodes that are in UMich barcode list, but not MSU database
# We don't have test information from MSU because UMich made them
umich_barcodes = list(set(lst) - set(tube_dict))
print("Number of tubes made at UMich: ",len(umich_barcodes))

counter=0
for barcode in umich_barcodes:
        tube = Tube()
        tube.set_ID(barcode)
        counter += 1
        # sleep every 1000 tubes to give the manager time to keep up
        if counter%1000 == 0:
                print("Processing tube ",counter," , ID ",barcode)
                #time.sleep(3)
        
        row = umich.index[(umich['tubeID'] == barcode).tolist()]
        tube = umich_tube_records(tube, row)

        # Adds tube with only UMich records
        database.add_tube(tube)

print("Finished! Now you have to wait for the manager to add all of the tubes")
old_database.close_shelve(tube_dict)


