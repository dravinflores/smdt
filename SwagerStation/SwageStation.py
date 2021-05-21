'''
Swage Station GUI
Created on Fri May 29 21:41:18 2020
Description: This code modifies and adds swage entries into the sMDT database.
While searching, previous results appear in the search frame and the previous 
values appear in the entry boxes. The code uses Tkinter for the graphical 
user interface and imports the sMDT database from a pickle file. 
To run, first instal Tkinter and pickle modules into your python library. After
that, running is as simple as: python "swage GUI.py" or double clicking in 
Windows 10. 
@author: Jason Gombas, Paul Johnecheck
'''




import tkinter as tk
from tkinter import StringVar
import pickle
import os
import sys
from datetime import datetime

DROPBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DROPBOX_DIR)
from sMDT import db, tube
from sMDT.data import swage



# Returns lengths, date, clean code, error code if avalible
def getInfo(code):
    try:
        database = db.db()
        tube1 = database.get_tube(code)
        record = tube1.swage.get_record()
        return [record.raw_length,record.swage_length],record.date, record.clean_code, record.error_code, ""
    except KeyError:
        return [],[],[],[],[]

def write(code, lengths, cleanCode, errorCode, name, endplugcode):
    database = db.db()
    tube1 = tube.Tube()
    tube1.m_tube_id = code
    tube1.swage.add_record(swage.SwageRecord(raw_length=lengths[0], swage_length=lengths[1], clean_code=cleanCode, error_code=errorCode, user=name))
    if endplugcode == "Munich":
        tube1.legacy_data['is_munich'] = True
    database.add_tube(tube1)
                        
#######################################
#####        Search Code       ########
####################################### 
def entry_update_search(sv):
    if sv.get() == '':
        button.configure(text='Create Entry')
        label_Search.configure(text="Search")
        entry_length.config(state=tk.NORMAL)
        view_Search.config(state=tk.NORMAL)
        option_cleancode.config(state=tk.NORMAL)
        view_Search.delete('1.0',tk.END)
        view_Search.config(state=tk.DISABLED)
        text_comment.delete("1.0", tk.END)
        sv_cleanCode.set("3: Only Vacuumed")
        sv_errorCode.set("0: No Error")
        return
    hasEntry = update_search(sv.get())
    lengths, date, cleanCode, errorCode, comment = getInfo(sv.get())
    if hasEntry and len(lengths)==2:
        entry_length.delete(0, tk.END)
        entry_length.insert(1,str(lengths[0]))
        entry_slength.delete(0, tk.END)
        entry_slength.insert(1,str(lengths[1]))
        button.configure(text="Update")
        #entry_length.config(state=tk.DISABLED)
        sv_cleanCode.set(cleanCode)
        option_cleancode.config(state=tk.DISABLED)
        sv_errorCode.set(errorCode)
        text_comment.delete("1.0",tk.END)
        text_comment.insert("1.0", comment)
        text_entryStatus.delete("1.0", tk.END)
        text_entryStatus.insert("1.0", "Entry already exists\nUpdate?")       
    else:
        button.configure(text="Create Entry")
        entry_length.config(state=tk.NORMAL)
        option_cleancode.config(state=tk.NORMAL)
        sv_cleanCode.set("3: Only Vacuumed")
        sv_errorCode.set("0: No Error")
        text_comment.delete("1.0", tk.END)
        text_entryStatus.delete("1.0", tk.END)
        #entry_length.delete(0, tk.END)
        #entry_slength.delete(0, tk.END)   

def update_search(code):
    printString = ''
    try:
        database = db.db()
        tube1 = database.get_tube(code)
        hasEntry = True
        printString = str(tube1)
    except KeyError:
        hasEntry = False
        printString = "No tube found with that barcode."
    printString+='\n\n\n'
    view_Search.config(state=tk.NORMAL)
    view_Search.delete('1.0',tk.END)
    view_Search.insert('1.0',printString)
    view_Search.config(state=tk.DISABLED)
    label_text = "Showing results for: " + code
    label_Search.configure(text=label_text)
    return hasEntry

#######################################
#####      Swage Entry Code    ########
#######################################    
def handle_enter(event):
    entry_name.config({"background": "White"})
    entry_barcode.config({"background": "White"})
    entry_length.config({"background": "White"})
    entry_slength.config({"background": "White"})
    text_comment.config({"background": "White"})

    if button.cget("text") == "Create Entry":
        status = True
        if not entry_length.get().replace('.', '', 1).replace('-', '', 1).isdigit():
            entry_length.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Lengths aren't numbers")
            status = False
        if not entry_slength.get().replace('.', '', 1).replace('-', '', 1).isdigit():
            entry_slength.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Lengths aren't numbers")
            status = False
        if sv_cleanCode.get()[0] == "1" and text_comment.get('1.0') == '':
            text_comment.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Add Comment")
            status = False
        if sv_errorCode.get()[0] == "1" and text_comment.get('1.0') == '':
            text_comment.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Add Comment")
            status = False
        if entry_name.get() == '':
            entry_name.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Fill in all fields")
            status = False
        if entry_barcode.get() == '':
            entry_barcode.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Fill in all fields")
            status = False
        if entry_length.get() == '':
            entry_length.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Fill in all fields")
            status = False
        if entry_slength.get() == '':
            entry_slength.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Fill in all fields")
            status = False
        if status:         
            name = entry_name.get()
            barcode = entry_barcode.get()
            firstLength = entry_length.get()
            secondLength = entry_slength.get()
            write(barcode, 
                  [firstLength,secondLength], 
                  sv_cleanCode.get(),
                  sv_errorCode.get(),
                  name,
                  sv_endplugCode.get())
            entry_barcode.delete(0, tk.END)
            entry_length.delete(0, tk.END)
            entry_slength.delete(0, tk.END)
            sv_cleanCode.set("3: Only Vacuumed")
            sv_errorCode.set("0: No Error")
            sv_endplugCode.set("Protvino")
            text_comment.delete("1.0", tk.END)
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", barcode + " was entered\ninto database")
            
    if button.cget("text") == "Update":
        status = True
        barcode = entry_barcode.get()
        if sv_cleanCode.get()[0] == "1" and text_comment.get('1.0') == '':
            text_comment.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Add Comment")
            status = False
        if sv_errorCode.get()[0] == "1" and text_comment.get('1.0') == '':
            text_comment.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Add Comment")
            status = False
        if not entry_length.get().replace('.', '', 1).replace('-','').isdigit():
            entry_length.config({"background": "Red"})
            text_entryStatus.delete("1.0", "4.29")
            text_entryStatus.insert("1.0", "Lengths aren't numbers")
            status = False
        if not entry_slength.get().replace('.', '', 1).replace('-','').isdigit():
            entry_slength.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            status = False
            text_entryStatus.insert("1.0", "Lengths aren't numbers")
        if entry_name.get() == '':
            entry_name.config({"background": "Red"})
            text_entryStatus.delete("1.0", tk.END)
            text_entryStatus.insert("1.0", "Fill in all fields")
            status = False
        if status:
                write(barcode, 
                  [entry_length.get(),entry_slength.get()],
                  sv_cleanCode.get(),
                  sv_errorCode.get(),
                  entry_name.get(),
                  sv_endplugCode.get())
                entry_barcode.delete(0, tk.END)
                entry_length.delete(0, tk.END)
                entry_slength.delete(0, tk.END)
                text_entryStatus.delete("1.0", tk.END)
                text_entryStatus.insert("1.0", barcode + " was updated")

filename = 'SwagerData\\' + f"{datetime.now().strftime('%m.%d.%Y_%H_%M_%S.csv')}"
window = tk.Tk()
window.title("Swage Station GUI")
window.columnconfigure(0, weight=1, minsize=75)
window.rowconfigure(0, weight=1, minsize=50)


########### Generate Frames ###############
frame_entry = tk.Frame(
            master=window,
            width = 25,
            relief=tk.RAISED,
            borderwidth=1
        )
frame_entry.grid(row=0, column=0)

frame_search = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
frame_search.grid(row=0, column=1)

sub_frame_search = tk.Frame(master=frame_search, relief=tk.RAISED)

########### Entry Frame ###############
label_name = tk.Label(master=frame_entry, text="Name")
entry_name = tk.Entry(master=frame_entry)

label_barcode = tk.Label(master=frame_entry, text="Barcode")
sv_barcode = StringVar()
sv_barcode.trace("w", lambda name, index, mode, 
                 sv_barcode=sv_barcode: entry_update_search(sv_barcode))
entry_barcode = tk.Entry(master=frame_entry, textvariable=sv_barcode)

label_length = tk.Label(master=frame_entry, text='Raw Length')
entry_length = tk.Entry(master=frame_entry)

label_slength = tk.Label(master=frame_entry, text='Swage Length')
entry_slength = tk.Entry(master=frame_entry)

label_cleancode = tk.Label(master=frame_entry, text='Clean Code')
sv_cleanCode = StringVar(window)
cleanOptions = ["0: Not Cleaned",
                "1: Cleaning described in comment",
                "2: Wiped with Ethanol",
                "3: Only Vacuumed",
                "4: Vacuumed and Wiped with Ethanol",
                "5: Vacuumed with Nitrogen"]
sv_cleanCode.set("3: Only Vacuumed")
option_cleancode = tk.OptionMenu(frame_entry, 
                                 sv_cleanCode,
                                 *cleanOptions)

label_errorcode = tk.Label(frame_entry, text='Error Code')
sv_errorCode = StringVar(window)
errorOptions = ["0: No Error",
                "1: Error Described in Comment",
                "2: Swaged Improperly",
                "3: Wire Snapped", 
                "4: Damaged wire couldn't tension",
                "5: Wire lost inside swaged tube",
                "6: Ferrule bumped after tensioning",
		"7: 0.8mm shim fits",
		"8: 1.6mm shim fits",
		"9: 2.4mm shim fits"]
sv_errorCode.set("0: No Error")
option_errorcode = tk.OptionMenu(frame_entry, sv_errorCode, *errorOptions)


label_endplugcode = tk.Label(frame_entry, text='End plug type')
sv_endplugCode = StringVar(window)
endplugOptions = ["Protvino",
		  "Munich"]
sv_endplugCode.set("Protvino")
option_endplugcode = tk.OptionMenu(frame_entry, sv_endplugCode, *endplugOptions)

label_comment = tk.Label(master=frame_entry, text='Comment')
text_comment = tk.Text(master=frame_entry,
                       width=30,
                       height=4)

button = tk.Button(
    master=frame_entry,
    text="Create Entry",
    width=33,
    height=2,
    bg="blue",
    fg="yellow",
)
button.bind("<Button-1>", handle_enter)
text_entryStatus = tk.Text(master=frame_entry, width=30, height=2)

############ Search Frame ###################
label_Search = tk.Label(master=frame_search, text='Search Tubes')
view_Search = tk.Text(master=frame_search)

label_s = tk.Label(master=sub_frame_search, text="Barcode: ")
#label_s.grid(row=0,column=0)
#entry_search = tk.Entry(master=sub_frame_search)
#entry_search.grid(row=0,column=1)
#button_search = tk.Button(master=sub_frame_search, text="Search")
#button_search.grid(row=0,column=2)
#button_search.bind("<Button-1>", update_search)

############  Pack Everything Together  ##########
entry = tk.Entry()
label_name.pack()
entry_name.pack()

label_barcode.pack()
entry_barcode.pack()

label_length.pack()
entry_length.pack()

label_slength.pack()
entry_slength.pack()

label_cleancode.pack()
option_cleancode.pack()

label_errorcode.pack()
option_errorcode.pack()

label_endplugcode.pack()
option_endplugcode.pack()

label_comment.pack()
text_comment.pack()

button.pack()
text_entryStatus.pack()

label_Search.pack()
view_Search.pack()
sub_frame_search.pack()

# Execute mainloop
window.mainloop()
