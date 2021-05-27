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
import sys

DROPBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DROPBOX_DIR)
from sMDT import db, tube
from sMDT.data import swage
from sMDT.data.status import Status

# Returns a list of the status of the tube, in this order:
# swage status, tension status, leak status, dark current status
def getStatus(code):
    #raise NotImplementedError
    #return 1 # for now, this is not implemented correctly
    try:
        database = db.db()
        tube1 = database.get_tube(code)
        sStatus = tube1.swage.status()
        tStatus = tube1.tension.status()
        lStatus = tube1.leak.status()
        dStatus = tube1.dark_current.status()
        return [sStatus, tStatus, lStatus, dStatus]
    except KeyError:
        return [Status.INCOMPLETE,Status.INCOMPLETE,Status.INCOMPLETE,Status.INCOMPLETE]

# Returns a list of the data of the tube, in this order:
# swage status, tension status, leak status, dark current status
def getData(code):
    #raise NotImplementedError
    #return 1 # for now, this is not implemented correctly
    data = [None, None, None, None]
    try:
        database = db.db()
        tube1 = database.get_tube(code)
        try:
            tRecord_first = tube1.tension.get_record()
            tRecord_last = tube1.tension.get_record()
            data[0] = tRecord_first.date
            data[1] = tRecord_last.tension
            data[2] = tRecord_last.date
            data[3] = tRecord_last.frequency
        except:
            data[0] = None
        try:
            data[4] = tube1.dark_current.get_record().dark_current
        except:
            data[4] = None
        return data
    except KeyError:
        return data
    

# Returns booleans to indicate which tests failed
def getFailedTests(code):
    try:
        database = db.db()
        tube1 = database.get_tube(code)
        sfail = tube1.swage.fail()
        tfail = tube1.tension.fail()
        lfail = tube1.leak.fail()
        dfail = tube1.dark_current.fail()
        return sfail,tfail,lfail,dfail
    except KeyError:
        return True,True,True,True

# Returns a list of barcodes found in the text
def textToList(barcodeList):
    if '\n' in barcodeList:
    	barcodeList.replace('\n','')
    lenBarcodes = int(len(barcodeList)/8)
    barcodes = [barcodeList[i*8:i*8+8] for i in range(lenBarcodes)]
    return list(filter(lambda a: a != '', barcodes))

# Check if one of the codes in the text is bad and display it
def checkCodes(barcodeList):
    barcodeList = text_list.get('1.0',tk.END)[0:-1]
    text_serrors.config(state=tk.NORMAL)
    text_serrors.delete("1.0", tk.END)
    text_terrors.config(state=tk.NORMAL)
    text_terrors.delete("1.0", tk.END)
    text_lerrors.config(state=tk.NORMAL)
    text_lerrors.delete("1.0", tk.END)
    text_derrors.config(state=tk.NORMAL)
    text_derrors.delete("1.0", tk.END)
    barcodes = textToList(barcodeList)

    text_serrors.insert(tk.INSERT, 'Failed:\n')
    text_terrors.insert(tk.INSERT, 'Failed:\n')
    text_lerrors.insert(tk.INSERT, 'Failed:\n')
    text_derrors.insert(tk.INSERT, 'Failed:\n')
    for tube in barcodes:
        sfail, tfail, lfail, dfail = getFailedTests(tube)
        if sfail:
            text_serrors.insert(tk.INSERT, tube)
        if tfail:
            text_terrors.insert(tk.INSERT, tube)
        if lfail:
            text_lerrors.insert(tk.INSERT, tube)
        if dfail:
            text_derrors.insert(tk.INSERT, tube)

    text_serrors.insert(tk.INSERT, '\nIncomplete:\n')
    text_terrors.insert(tk.INSERT, '\nIncomplete:\n')
    text_lerrors.insert(tk.INSERT, '\nIncomplete:\n')
    text_derrors.insert(tk.INSERT, '\nIncomplete:\n')
    for tube in barcodes:
        status = getStatus(tube)
        if status[0] == Status.INCOMPLETE:
            text_serrors.insert(tk.INSERT, tube)
        if status[1] == Status.INCOMPLETE:
            text_terrors.insert(tk.INSERT, tube)
        if status[2] == Status.INCOMPLETE:
            text_lerrors.insert(tk.INSERT, tube)
        if status[3] == Status.INCOMPLETE:
            text_derrors.insert(tk.INSERT, tube)

    text_serrors.config(state=tk.DISABLED)
    text_terrors.config(state=tk.DISABLED)
    text_lerrors.config(state=tk.DISABLED)
    text_derrors.config(state=tk.DISABLED)

# Write data for tubes to disk
def write(name, barcodeList):
    #raise NotImplementedError
    filename = DROPBOX_DIR + "\\Exported_Tubes\\" + f"{datetime.now().strftime('%m.%d.%Y_%H_%M_%S.csv')}"
    filename  = "Exported_Tubes/" + f"{datetime.now().strftime('%m.%d.%Y_%H_%M_%S.csv')}"
    f = open(filename,'w')

    f.write("Logger,Barcode,First Tension Date,Final Tension Measurement,Dark Current\n")
    barcodes = textToList(barcodeList)
    badTubeList = []
    for code in barcodes:
        data = getData(database,code)
        f.write(f"{name},{code},{data[0]},{data[1]},{data[2]}\n")
    return badTubeList

#######################################
#####   Submit Codes to Export ########
#######################################    
def handle_enter(event):
    text_serrors.config(state=tk.NORMAL)
    text_serrors.delete("1.0", tk.END)  # Turn text editing on and clear the textbox
    text_terrors.config(state=tk.NORMAL)
    text_terrors.delete("1.0", tk.END)
    text_lerrors.config(state=tk.NORMAL)
    text_lerrors.delete("1.0", tk.END)
    text_derrors.config(state=tk.NORMAL)
    text_derrors.delete("1.0", tk.END)


    entry_name.config({"background": "White"})
    if entry_name.get() == '':
        entry_name.config({"background": "Red"})
    else:
        name = entry_name.get()
        barcodeList = text_list.get('1.0',tk.END)[0:-1]
        write(name, barcodeList)
        text_list.delete("1.0", tk.END)
        text_serrors.insert('1.0',"Tubes \nwritten")
    text_serrors.config(state=tk.DISABLED)

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

############ Swage Error Frame ################
label_serrors = tk.Label(master=frame_error, text='Swage \n Errors')
text_serrors = tk.Text(master=frame_error,
                       width=8,
                       height=30)
text_serrors.config(state=tk.DISABLED)

############ Tension Error Frame ################
label_terrors = tk.Label(master=frame_error, text='Tension \n Errors')
text_terrors = tk.Text(master=frame_error,
                       width=8,
                       height=30)
text_terrors.config(state=tk.DISABLED)

############ Leak Rate Error Frame ################
label_lerrors = tk.Label(master=frame_error, text='Leak Rate \n Errors')
text_lerrors = tk.Text(master=frame_error,
                       width=8,
                       height=30)
text_lerrors.config(state=tk.DISABLED)

############ Dark Current Error Frame ################
label_derrors = tk.Label(master=frame_error, text='Dark C\n Errors')
text_derrors = tk.Text(master=frame_error,
                       width=8,
                       height=30)
text_derrors.config(state=tk.DISABLED)

############  Pack Everything Together  ##########
entry = tk.Entry()
label_name.pack()
entry_name.pack()

label_list.pack()
text_list.pack()

label_serrors.grid(row=0,column=0)
text_serrors.grid(row=1,column=0)
label_terrors.grid(row=0,column=1)
text_terrors.grid(row=1,column=1)
label_lerrors.grid(row=0,column=2)
text_lerrors.grid(row=1,column=2)
label_derrors.grid(row=0,column=3)
text_derrors.grid(row=1,column=3)

button.pack()

# Execute mainloop
window.mainloop()
