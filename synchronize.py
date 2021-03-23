import os
import pickle
from glob import glob
from collections import defaultdict
from datetime import datetime, timedelta
import re


def synchronize():
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    database = defaultdict(lambda: defaultdict(list))
    ##########Swager Station#############
    filenames = glob(os.path.join(DIR_PATH, 'SwagerStation/SwagerData/*'))
    for filename in filenames:
        with open(filename) as file:              ## Jason added the date to the data collected at the swager station
            m = re.search('\d+.\d+.\d+',filename)
            if m is not None:
                 date = m.group(0)
            else:
                date = 'Not Avalible'

            for line in file:
                if line:
                    sDate = date
                    line = line.split(',')
                    rawLength = ''
                    swageLength = ''
                    if len(line) == 9:
                        barcode = line[0].replace('\r\n', '')
                        rawLength = line[1]
                        swageLength = line[2]
                        comment = line[6]
                        user    = line[-2].replace('\r\n', '')
                        eCode = line[5]
                        cCode = line[4]
                        sDate = line[3]
                    elif len(line) == 8:
                        barcode = line[0].replace('\r\n', '')
                        rawLength = line[1]
                        swageLength = line[2]
                        comment = line[6]
                        user    = line[-1].replace('\r\n', '')
                        eCode = line[5]
                        cCode = line[4]
                        sDate = line[3]
                    else:
                        barcode = line[0].replace('\r\n', '')
                        comment = line[0]
                        user    = line[-1].replace('\r\n', '')
                        eCode = "Unknown"
                        cCode = "Unknown"
                        sDate = date
                    database[barcode]['swagerUser'].append(user)
                    database[barcode]['rawLength'].append(rawLength)
                    database[barcode]['swageLength'].append(swageLength)
                    database[barcode]['swagerComment'].append(comment)
                    database[barcode]['swagerDate'].append(sDate)
                    database[barcode]['swagerFile'].append(filename)
                    database[barcode]['eCode'].append(eCode)
                    database[barcode]['cCode'].append(cCode)
                    for comment in database[barcode]['swagerComment']:
                        if 'bad' in comment or 'snapped' in comment or 'broke' in comment:
                            database[barcode]['failsSwager'] = True
                        else:
                            database[barcode]['failsSwager'] = False
    print("Done with swager data")


    #########Tension Station#############
    ## First extract all the data from the data files
    filenames = glob(os.path.join(DIR_PATH, 'TensionStation/output/*'))
    for filename in filenames:
        with open(filename) as file:
            next(file)
            for line in file:
                line = line.split(',')
                if len(line) < 6:      ## Added so that it wouldn't crash with tubes.csv was '== 2'
                    break
                user      = line[0]
                dateTime  = line[1]
                barcode   = line[2]
                length    = float(line[3])
                frequency = float(line[5])
                tension   = float(line[6])
                if tension == 0:
                    continue
                database[barcode]['tensionUser'].append(user)
                database[barcode]['tensionDateTime'].append(dateTime)
                database[barcode]['tensionLength'].append(length)
                database[barcode]['frequency'].append(frequency)
                database[barcode]['tensions'].append(tension)
                database[barcode]['tensionFile'].append(filename)

    ## Next, sort tensions into first tensions and second tensions
    for code, tubeData in database.items():
        for i, tension in enumerate(database[code]['tensions']):
            dates = [datetime.strptime(date, '%d.%m.%Y %H.%M.%S') for date in database[code]['tensionDateTime']]
            if abs(dates[i] - min(dates)) < timedelta(days=9):
                database[code]['firstTensions'].append(tension)
                database[code]['firstTensionUsers'].append(database[code]['tensionUser'][i])
                database[code]['firstTensionDates'].append(database[code]['tensionDateTime'][i])
                if abs(tension - 350.) > 15:
                    if 'failsFirstTension' not in database[code].keys():
                        database[code]['failsFirstTension'] = True
                else:
                    database[code]['failsFirstTension'] = False
            else:
                database[code]['secondTensions'].append(tension)
                database[code]['secondTensionUsers'].append(database[code]['tensionUser'][i])
                database[code]['secondTensionDates'].append(str(database[code]['tensionDateTime'][i])) 
                if abs(tension - 350.) > 15:
                    if 'failsSecondTension' not in database[code].keys():
                        database[code]['failsSecondTension'] = True
                    else:
                        database[code]['failsSecondTension'] = False
                else:
                    database[code]['failsSecondTension'] = False
     
     
    for code, tubeData in database.items():
            firstMeasures = database[code]['firstTensions']
            secondMeasures = database[code]['secondTensions']
            tensions = database[code]['tensions']
            frequencies = database[code]['frequency']
            dates = database[code]['tensionDateTime']
            if len(firstMeasures) > 0:
                database[code]["firstTension"] = min(firstMeasures, key=lambda x: abs(x-350))
                database[code]["firstTensionDate"] = dates[tensions.index(database[code]["firstTension"])]
                database[code]["firstFrequency"] = frequencies[tensions.index(database[code]["firstTension"])]
            if len(secondMeasures) > 0:
                database[code]["secondTension"] = min(secondMeasures, key=lambda x: abs(x-350))
                database[code]["secondTensionDate"] = dates[tensions.index(database[code]["secondTension"])]
                database[code]["secondFrequency"] = frequencies[tensions.index(database[code]["secondTension"])]
    ## Finally, check which tubes are ready for second tension
    #for code, tubeData in database.items():      
    #    if len(database[code]['tensions']) == 0:
    #        database[code]['secondTensionReady'] = False
    #        continue
    #    firstTension = min(database[code]['firstTensions'], key=lambda x: abs(x-350))
    #    dates = [datetime.strptime(date, '%d.%m.%Y %H.%M.%S') for date in database[code]['tensionDateTime']]
    #    if datetime.today() - dates[database[code]['tensions'].index(firstTension)] > timedelta(days=12):
    #        if 'secondTensionReady' not in database[code].keys():
    #            database[code]['secondTensionReady'] = False
    #        else:
    #            database[code]['secondTensionReady'] = True
    print("Done with tension")              
             

    ####### leak detector #################3
    filenames = glob(os.path.join(DIR_PATH, 'LeakDetector/*'))
    for filename in filenames:
        barcode = os.path.basename(filename.replace('.txt','')).split('_')[0]
        with open(filename) as file:
            for line in file:
                line = line.split('\t')
                if len(line[0].split('E')) == 2: 
                    leakRate = float(line[0].split('E')[0])*10**float(line[0].split('E')[1])
                elif not line[0]:
                    continue
                else:
                    print(filename)
                    leakRate = float(line[2])
                leakStatus = line[2]
                
                database[barcode]['leakRate'].append(leakRate)
                database[barcode]['leakStatus'].append(leakStatus)
                database[barcode]['leakFile'].append(filename)
                 

                if len(line) > 3:
                    dateTime = line[3] + ' ' + line[4][:-3]
                    if len(line[4]) >8: datetime_obj = datetime.strptime(dateTime, '%m/%d/%Y %H:%M:%S')
                    else: datetime_obj = datetime.strptime(dateTime, '%m/%d/%Y %H:%M')
                    if line[4][-2:] == 'PM':
                        datetime_obj = datetime_obj + timedelta(hours=12)
                    dateTime = datetime_obj.strftime('%d.%m.%y %H.%M.00')
                    database[barcode]['leakDateTime'].append(dateTime)

                if len(line) > 5:
                    user = line[5]
                    database[barcode]['leakUser'].append(user)
                
                if leakRate > 1E-5:
                    database[barcode]['failsLeak'] = True
                else:
                    database[barcode]['failsLeak'] = False
    print("Done with leak data")
    
    ####### dark current #################
    filenames = glob(os.path.join(DIR_PATH, 'DarkCurrent/3015V Dark Current/*'))
    for filename in filenames:
        with open(filename) as file:
            code = filename.replace('.csv','')
            code = code[-8:]
            currents = []
            dates = []
            for line in file:
                sp = line.split(',')
                currents.append(sp[0])
                dates.append(sp[1])
            database[code]['currentTestDates'] = dates
            database[code]['currentFile'] = filename
            database[code]['darkCurrents'] = currents
            if float(currents[-1]) > 2:
                database[code]['failsCurrent'] = True

    print("Done with dark current data")
    
    ## Loop over to sort good tubes from bad tubes. 'Uncertain' tubes remain empty        
    for code, tubeData in sorted(database.items(), reverse=True):
        if code < 'MSU00500':
            continue
        #print(code + ': ' + str(database[code]['failsCurrent']))
        for code in tubeData['eCode']:
            if code[0] != 'U':
                codeNum = int(code[0])
                if codeNum > 0 and codeNum<6:
                    tubeData['good'] = False
                    continue
        if not tubeData['tensions'] and not tubeData['darkCurrents'] and not tubeData['leakRate']:
            tubeData['good'] = False
        elif 'failsSwager' in tubeData.keys() and tubeData['failsSwager'] == True:
            tubeData['good'] = False
        elif 'failsFirstTension' in tubeData.keys() and tubeData['failsFirstTension'] == True:
            tubeData['good'] = False
        elif 'failsSwager' not in tubeData.keys() or \
             'failsLeak' not in tubeData.keys():
            continue
        elif tubeData['failsSwager'] or tubeData['failsFirstTension'] \
          or tubeData['failsLeak'] or 'failsCurrent' in tubeData.keys():
            tubeData['good'] = False
        elif 'failsSecondTension' not in tubeData.keys():
            continue
        elif tubeData['failsSecondTension']:
            tubeData['good'] = False
        else:
            tubeData['good'] = True
    print("Sorted good from bad")

    #convert defaulctdict of defaultdicts to simple dict of dicts
    conv_database = {}
    for tube, data in database.items():
        conv_database[tube] = dict(data)
    pickle.dump(conv_database, open('database.p', 'wb'))
    print("Conversion complete")

    ## Write most recent entries into readable text file
#    secondTensionReady = []
#    file = open("Database_Entries.txt","w")
#    file.write('  Code   |Name\t|Date \t|T1  |f1   |Date  |T2  |f2   |Date  |Leak\t|Dark\t|L1  \t|L2  \t|Comments\n')
#    for code, tubeData in sorted(database.items(), reverse=True):
#        if not code.endswith('\n'):
#            firstFrequency = tubeData.get('firstFrequency')
#            secondFrequency = tubeData.get('secondFrequency')
#            firstTension = tubeData.get('firstTension')
#            secondTension = tubeData.get('secondTension')
#            firstDate = tubeData.get('firstTensionDate')
#            secondDate = tubeData.get('secondTensionDate')
#
#                
#            printString = code[3:] + '  '
#            if 'swagerUser' in database[code].keys():
#                printString += database[code]['swagerUser'][0][0:4] + '  \t'
#                printString += database[code]['swagerDate'][0][0:-5].replace('.','/') + '\t'
#            else:
#                printString += 'none\tnone \t'
#    
#            if firstTension != 0:
#                printString += str(firstTension)[0:3] + '  '
#                printString += str(firstFrequency)[0:4] + '  '
#                printString += str(firstDate)[3:5] + '/' + str(firstDate)[0:2] + '  '
#            else:
#                printString += 'None              '
#
#            if secondTension != 0:
#                printString += str(secondTension)[0:3] + '  '
#                printString += str(secondFrequency)[0:4] + '  '
#                printString += str(secondDate)[3:5] + '/' + str(secondDate)[0:2] + '  '
#            else:
#                printString += 'None              '
#    
#            if 'leakUser' in database[code].keys():
#                printString += '%.1E' % min([i for i in database[code]['leakRate']])
#            else:
#                printString += 'None'
#
#            if 'testType' in database[code].keys():
#                if database[code]['testType'] == 'single':
#                    printString += '\t%.1fS\t' % float (database[code]['finalCurrent'])
#                else:
#                    printString += '\t%.1fM\t' % float (database[code]['finalCurrent'])
#            else:
#                printString += '\tNone\t'
#                
#            if 'rawLength' in database[code].keys():
#                printString += database[code]['rawLength'][-1] + '\t'
#            if 'swageLength' in database[code].keys():
#                printString += database[code]['swageLength'][-1] + '\t'
#            if 'swagerComment' in database[code].keys():
#                for comment in database[code]['swagerComment']:
#                    printString += comment + '\t'
#            if tubeData['good'] == False:
#                file.write('B ' + printString + '\n')
#            elif tubeData['good'] == True:
#                   file.write('G ' + printString + '\n')
#            else:
#                file.write('U ' + printString + '\n')
#                
#            if code in secondTensionReady:
#                secondTensionReady.remove(code)

    file.close()

    ## Write a file that lists the tubes ready for second tenison
    #file = open("SecondTensionReady.txt","w")
    #file.write('Tubes up for second tension test:\n')
    #for tube, tubeData in sorted(database.items(), reverse=True):
    #    if tubeData['secondTensionReady'] and tubeData['secondTension'] == []:
    #        file.write(tube + '\n')

    return conv_database


if __name__ == '__main__':
    synchronize()
