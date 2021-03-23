# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 19:27:48 2020

@author: Jason
"""

import pickle
import matplotlib.pyplot as plt
import datetime
import os
import time
import synchronize

def removeDuplicates(aList):
    return(list(set(aList)))

def tubeStats():
	database = pickle.load(open('database.p', 'rb'))
	message = ''
	FailFirstTension = []
	FailSecondTension = []
	FailCurrent = []
	NoTension = []
	NoLeak = []
	NoCurrent = []
	Unknown = []
	firstHist = []
	secondHist = []
	firstHistBad = []
	secondHistBad = []
	diff = []
	diffBad = []
	firstHistBadName = []
	error1 = []
	error2 = []
	error3 = []
	error4 = []
	error5 = []
	error6 = []
	biggestCode = 'MSU00'
	totalTubes = 0
	uncertainTubes = 0
	for tube, tubeData in sorted(database.items(), reverse=True):
	    if tube > biggestCode:
	        biggestCode = tube
	    if tube:
	        if 'swagerDate' not in tubeData.keys(): continue
	        dateString = tubeData['swagerDate'][-1]
	        if dateString == 'Not Avalible': continue
	        date = datetime.date(int(dateString[6:10]),int(dateString[0:2]),int(dateString[3:5]))
	        twoWeeksAgo = datetime.date.today() - datetime.timedelta(days=14)
	        if date >= twoWeeksAgo:
	            totalTubes += 1
	            for error in tubeData['eCode']:
	                if error[0] == '1': error1.append(tube)
	                if error[0] == '2': error2.append(tube)
	                if error[0] == '3': error3.append(tube)
	                if error[0] == '4': error4.append(tube)
	                if error[0] == '5': error5.append(tube)
	                if error[0] == '6': error6.append(tube)
	            if 'good' in tubeData and tubeData['good'] == False:                
	                if 'failsFirstTension' in tubeData.keys() and tubeData['failsFirstTension'] == True:     
	                    FailFirstTension.append(tube)
	                elif 'failsSecondTension' in tubeData.keys() and tubeData['failsSecondTension'] == True: 
	                    FailSecondTension.append(tube)
	                elif 'failsCurrent' in tubeData.keys() and tubeData['failsCurrent'] == True:             
	                    FailCurrent.append(tube)
	                elif 'firstTensions' not in tubeData.keys() or tubeData['firstTensions'] == []:          
	                    NoTension.append(tube)
	                elif 'leakRate' not in tubeData.keys() or tubeData['leakRate'] == []:                    
	                    NoLeak.append(tube)
	                elif 'finalCurrent' not in tubeData.keys():                                              
	                    NoCurrent.append(tube)
	                else:                                                                                    
	                    Unknown.append(tube)
	            if 'good' not in tubeData.keys(): 
	                uncertainTubes +=1

	error1 = removeDuplicates(error1)
	error2 = removeDuplicates(error2)
	error3 = removeDuplicates(error3)
	error4 = removeDuplicates(error4)
	error5 = removeDuplicates(error5)
	error6 = removeDuplicates(error6)

	error2 = [item for item in error2 if item not in set(error1)]
	error3 = [item for item in error3 if item not in (set(error1)|set(error2))]
	error4 = [item for item in error4 if item not in (set(error1)|set(error2)|set(error3))]
	error5 = [item for item in error5 if item not in (set(error1)|set(error2)|set(error3)|set(error4))]
	error6 = [item for item in error6 if item not in (set(error1)|set(error2)|set(error3)|set(error4)|set(error5))]


	tubesWithErrorCode = list(set(error1)|set(error2)|set(error3)|set(error4)|set(error5)|set(error6))
	tubesThatFailed = list(set(FailFirstTension)|set(FailSecondTension)|set(FailCurrent)|set(NoTension)|set(NoLeak)\
	                            |set(NoCurrent)|set(Unknown))

	message += "Of " + str(totalTubes) + '\n'
	message += "Good (potentially) tubes: " + str(totalTubes - len(tubesThatFailed)) + '\n'
	message += "Bad tubes: " + str(len(tubesThatFailed)) + '\n'
	message += str(uncertainTubes) + ' tubes that require a QC test' + '\n'
	message += "Total Failure Rate: " + str(len(tubesThatFailed)/totalTubes*100) + "%\n"
	
	exECodesFailFirstTension = [item for item in FailFirstTension if item not in tubesWithErrorCode]
	exECodesFailSecondTension = [item for item in FailSecondTension if item not in tubesWithErrorCode]
	exECodesFailCurrent = [item for item in FailCurrent if item not in tubesWithErrorCode]
	exECodesNoTension = [item for item in NoTension if item not in tubesWithErrorCode]
	exECodesNoLeak = [item for item in NoLeak if item not in tubesWithErrorCode]
	exECodesNoCurrent = [item for item in NoCurrent if item not in tubesWithErrorCode]
	exECodesUnknown = [item for item in Unknown if item not in tubesWithErrorCode]

	if len(error1) > 0:
	    message += '\tError 1: Error Described in Comment - ' + str(len(error1)) + "     " + str(len(error1)/totalTubes*100) + "%" + '\n'
	    for error in sorted(error1):
	        user = database[error]['swagerUser'][0]
	        message += '\t\t' + error + ' - Swaged by ' + user + '\n'
	if len(error2) > 0:
	    message += '\tError 2: Swaged Improperly - ' + str(len(error2)) + "     " + str(len(error2)/totalTubes*100) + "%" + '\n'
	    for error in sorted(error2):
	        user = database[error]['swagerUser'][0]
	        message += '\t\t' + error + ' - Swaged by ' + user + '\n'
	if len(error3) > 0:
	    message += '\tError 3: Wire Snapped - ' + str(len(error3)) + "     " + str(len(error3)/totalTubes*100) + "%" + '\n'
	    for error in sorted(error3):
	        user = database[error]['swagerUser'][0]
	        message += '\t\t' + error + ' - Swaged by ' + user + '\n'
	if len(error4) > 0:
	    message += '\tError 4: Damaged wire; couldn\'t tension - ' + str(len(error4)) + "     " + str(len(error4)/totalTubes*100) + "%" + '\n'
	    for error in sorted(error4):
	        user = database[error]['swagerUser'][0]
	        message += '\t\t' + error + ' - Swaged by ' + user + '\n'
	if len(error5) > 0:
	    message += '\tError 5: Wire lost inside swaged tube - ' + str(len(error5)) + "     " + str(len(error5)/totalTubes*100) + "%" + '\n'
	    for error in sorted(error5):
	        user = database[error]['swagerUser'][0]
	        message += '\t\t' + error + ' - Swaged by ' + user + '\n'
	if len(error6) > 0:
	    message += '\tError 6: Ferrule bumped after tensioning - ' + str(len(error6)) + "     " + str(len(error6)/totalTubes*100) + "%" + '\n'
	    for error in sorted(error6):
	        user = database[error]['swagerUser'][0]
	        message += '\t\t' + error + ' - Swaged by ' + user + '\n'

	if len(exECodesFailFirstTension) > 0:
	    message += '\tFails 1st Tension: ' + str(len(exECodesFailFirstTension)) + "     " + str(len(exECodesFailFirstTension)/totalTubes*100) + "%" + '\n'
	    for tube in sorted(exECodesFailFirstTension):
	        user = database[tube]['tensionUser'][0]
	        message += '\t\t' + tube + ' - Tensioned by ' + user + '\n'
	if len(exECodesFailSecondTension) > 0:
	    message += '\tFails 2nd Tension: ' + str(len(exECodesFailSecondTension)) + "     " + str(len(exECodesFailSecondTension)/totalTubes*100) + "%" + '\n'
	    for tube in sorted(exECodesFailSecondTension):
	        user = database[tube]['tensionUser'][0]
	        message += '\t\t' + tube + ' - Tensioned by ' + user + '\n'
	if len(exECodesFailCurrent) > 0:
	    message += '\tFails Current: ' + str(len(exECodesFailCurrent)) + "     " + str(len(exECodesFailCurrent)/totalTubes*100) + "%" + '\n'
	    for tube in sorted(exECodesFailCurrent):
	        user = database[tube]['swagerUser'][0]
	        message += '\t\t' + tube + ' - Swaged by ' + user + '\n'
	if len(exECodesNoTension) > 0:
	    message += '\tNumber without First Tension: ' + str(len(exECodesNoTension)) + "     " + str(len(exECodesNoTension)/totalTubes*100) + "%" + '\n'
	    for tube in sorted(exECodesNoTension):
	        user = database[tube]['swagerUser'][0]
	        message += '\t\t' + tube + ' - Swaged by ' + user + '\n'
	if len(exECodesNoLeak) > 0:
	    message += '\tNumber without Leak Rate: ' + str(len(exECodesNoLeak)) + "     " + str(len(exECodesNoLeak)/totalTubes*100) + "%" + '\n'
	    for tube in sorted(exECodesNoLeak):
	        user = database[tube]['swagerUser'][0]
	        message += '\t\t' + tube + ' - Swaged by ' + user + '\n'
	if len(exECodesNoCurrent) > 0:
	    message += '\tNumber without Current: ' + str(len(exECodesNoCurrent)) + "     " + str(len(exECodesNoCurrent)/totalTubes*100) + "%" + '\n'
	    for tube in sorted(exECodesNoCurrent):
	        user = database[tube]['swagerUser'][0]
	        message += '\t\t' + tube + ' - Swaged by ' + user + '\n'
	if len(exECodesUnknown) > 0:
	    message += '\tNumber Unknown Failure: ' + str(len(exECodesUnknown)) + "     " + str(len(exECodesUnknown)/totalTubes*100) + "%" + '\n'
	    for tube in exECodesUnknown:
	        user = database[tube]['swagerUser'][0]
	        message += '\t\t' + tube + ' - Swaged by ' + user + '\n'
	return message

if __name__ == '__main__':
	while 1:
		synchronize.synchronize()
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Tube statistics on past 2 weeks\nUpdates every 60s: \n\n")
		print(tubeStats())
		time.sleep(60)
