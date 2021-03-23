# -*- coding: utf-8 -*-

'''
Export GUI

Description: This script will write the exported tubes into a csv file so that
tubes can be tracked as they are exported to UMich. This script also checks
if one of the tubes have not passed a test. It will notify the user that one
of the tests has not been passed. 

To run, first install Tkinter and pickle modules into your python library. After
that, running is as simple as: python "Export_Tubes.py" or double clicking in 
Windows 10. 

@author: Jason Gombas
'''

import tkinter as tk
from tkinter import StringVar
import os
from datetime import datetime
import pickle
import time

path = "C:\\Users\\Swager\\Dropbox\\sMDT\\"

# Loads and returns the database as a dictionary
def loadDatabase():
    return pickle.load(open(path+'database.p', 'rb'))
    #return pickle.load(open(path+'/database.p', 'rb'))

# Returns a list of barcodes found in the text
def textToList(barcodeList):
    if '\n' in barcodeList:
    	barcodeList.replace('\n','')
    lenBarcodes = int(len(barcodeList)/8)
    barcodes = [barcodeList[i*8:i*8+8] for i in range(lenBarcodes)]
    return list(filter(lambda a: a != '', barcodes))

# Determines if the tube has all the required data
def isTubeBad(code):
    data = []
    if code not in database.keys(): 
    	return True
    if 'good' not in database[code].keys():
        return True
    if database[code]['good']==False:
        return True
    if 'firstTension' not in database[code].keys():
        return True
    if 'secondTension' not in database[code].keys():
        return True
    if 'darkCurrents' not in database[code].keys():
        return True
    if 'leakRate' not in database[code].keys():
        return True
    return False

# Get Data returns 1st Tension, 2nd Tension, Dark Current, and Leak Rate
def getData(database, code):
    data = []
    data.append(database[code]['firstTension'])
    data.append(database[code]['secondTension'])
    data.append(database[code]['darkCurrents'][-1])
    data.append(database[code]['leakRate'][-1])
    return data

# Check if one of the codes in the text is bad and display it
def checkCodes(barcodeList):
    barcodeList = text_list.get('1.0',tk.END)[0:-1]
    text_errors.config(state=tk.NORMAL)
    text_errors.delete("1.0", tk.END)
    barcodes = textToList(barcodeList)
    for tube in barcodes:
        if isTubeBad(tube):
            text_errors.insert(tk.INSERT, tube)
    text_errors.config(state=tk.DISABLED)

# Write data for tubes to disk
def write(name, barcodeList):
    filename = path + "Exported_Tubes\\" + f"{datetime.now().strftime('%m.%d.%Y_%H_%M_%S.csv')}"
    #filename  = "Exported_Tubes/" + f"{datetime.now().strftime('%m.%d.%Y_%H_%M_%S.csv')}"
    f = open(filename,'w')

    f.write("Logger,Barcode,First Tension,Second Tension,Dark Current,Leak Rate\n")
    barcodes = textToList(barcodeList)
    database = loadDatabase()
    badTubeList = []
    for code in barcodes:
        if isTubeBad(code):
            badTubeList.append(code)
            f.write(f"{name},{code} ERROR, this tube has not passed a test\n")
        else:
            data = getData(database,code)
            f.write(f"{name},{code},{data[0]},{data[1]},{data[2]},{data[3]}\n")
    return badTubeList

#######################################
#####   Submit Codes to Export ########
#######################################    
def handle_enter(event):
    text_errors.config(state=tk.NORMAL)
    text_errors.delete("1.0", tk.END)  # Turn text editing on and clear the textbox

    entry_name.config({"background": "White"})
    status = True
    if entry_name.get() == '':
        entry_name.config({"background": "Red"})
        status = False
    if status:         
        name = entry_name.get()
        barcodeList = text_list.get('1.0',tk.END)[0:-1]
        badTubeList = write(name, barcodeList)
        text_list.delete("1.0", tk.END)
        if badTubeList != []:
            for i, tube in enumerate(badTubeList):
                text_errors.insert(tk.INSERT, tube)
        else:
            text_errors.insert('1.0',"Success!")
    text_errors.config(state=tk.DISABLED)

window = tk.Tk()
window.title("Export Log GUI")
window.columnconfigure(0, weight=1, minsize=75)
window.rowconfigure(0, weight=1, minsize=50)


########### Generate Frames ###############
frame_entry = tk.Frame(
            master=window,
            width = 20,
            relief=tk.RAISED,
            borderwidth=1
        )
frame_entry.grid(row=0,column=0)

frame_error = tk.Frame(master=window)
frame_error.grid(row=0,column=1)

########### Entry Frame ###############
label_name = tk.Label(master=frame_entry, text="Name")
entry_name = tk.Entry(master=frame_entry)

label_list = tk.Label(master=frame_entry, text='List of Tubes')
text_list = tk.Text(master=frame_entry,
                       width=8,
                       height=30)

text_list.bind('<KeyRelease>',checkCodes)

button = tk.Button(
    master=frame_entry,
    text="Submit Tubes",
    width=20,
    height=2,
    bg="blue",
    fg="yellow",
    )
button.bind("<Button-1>", handle_enter)

############ Error Frame ################
label_errors = tk.Label(master=frame_error, text='Bad tubes appear here:')
text_errors = tk.Text(master=frame_error,
                       width=8,
                       height=30)
text_errors.config(state=tk.DISABLED)

############  Pack Everything Together  ##########

entry = tk.Entry()
label_name.pack()
entry_name.pack()

label_list.pack()
text_list.pack()

label_errors.pack()
text_errors.pack()

button.pack()

database = loadDatabase()

# Execute mainloop
window.mainloop()
