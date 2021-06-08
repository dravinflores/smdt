'''
Comment GUI
Created on 
Description: 
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
from sMDT.data.status import ErrorCodes


def write(code, lengths, cleanCode, name):
    database = db.db()
    tube1 = tube.Tube()
    tube1.set_ID(code)
    tube1.swage.add_record(swage.SwageRecord(raw_length=float(lengths[0]), 
                                             swage_length=float(lengths[1]), 
                                             clean_code=cleanCode, 
                                             user=name))
    database.add_tube(tube1)
                    

#######################################
#####      Swage Entry Code    ########
#######################################    
def handle_enter(event):
    entry_name.config({"background": "White"})
    entry_barcode.config({"background": "White"})

    status = True

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

    if status:         
        name = entry_name.get()
        barcode = entry_barcode.get()
        comment = text_comment.get('1.0',tk.END)[0:-1]
        comment = comment.replace('\n','. ')
        errorCode = sv_errorCode.get()
        errorCode = errorCode.split(':')[0]
        errorCode = int(errorCode)

        database = db.db()
        tube2 = tube.Tube()
        tube2.set_ID(barcode)
        tube2.new_comment((comment, name, datetime.now(), ErrorCodes(errorCode)))
        database.add_tube(tube2)
        entry_barcode.delete(0, tk.END)
        sv_errorCode.set("0: NO_ERROR")
        text_entryStatus.delete("1.0", tk.END)
        text_entryStatus.insert("1.0", barcode + " was entered\ninto database")
        text_comment.delete("1.0", tk.END)

window = tk.Tk()
window.title("Comment GUI")
window.columnconfigure(0, weight=1, minsize=75)
window.rowconfigure(0, weight=1, minsize=50)


########### Generate Frames ###############
frame_entry = tk.Frame(
            master=window,
            width = 25,
            relief=tk.RAISED,
            borderwidth=1
        )
frame_entry.pack()

########### Entry Frame ###############
label_name = tk.Label(master=frame_entry, text="Name")
entry_name = tk.Entry(master=frame_entry)

label_barcode = tk.Label(master=frame_entry, text="Barcode")
entry_barcode = tk.Entry(master=frame_entry)

label_cleancode = tk.Label(master=frame_entry, text='Error Code')
sv_errorCode = StringVar(window)
errorOptions = [   "0: NO_ERROR",
                   "2: SWAGED_IMPROPERLY",
                   "3: WIRE_SNAPPED",
                   "4: DAMAGED_WIRE_COULDNT_TENSION",
                   "5: WIRE_LOST_IN_SWAGED_TUBE",
                   "6: FERRULE_BUMPED_AFTER_TENSIONING"]
sv_errorCode.set("0: NO_ERROR")
option_cleancode = tk.OptionMenu(frame_entry, 
                                 sv_errorCode,
                                 *errorOptions)

label_comment = tk.Label(master=frame_entry, text='Enter a comment here:')
text_comment = tk.Text(master=frame_entry,
                       width=30,
                       height=4)

button = tk.Button(
    master=frame_entry,
    text="Create Comment",
    width=33,
    height=2,
    bg="blue",
    fg="yellow",
)
button.bind("<Button-1>", handle_enter)
text_entryStatus = tk.Text(master=frame_entry, width=40, height=4)

############  Pack Everything Together  ##########
entry = tk.Entry()
label_name.pack()
entry_name.pack()

label_barcode.pack()
entry_barcode.pack()

label_cleancode.pack()
option_cleancode.pack()

label_comment.pack()
text_comment.pack()

button.pack()
text_entryStatus.pack()


# Execute mainloop
window.mainloop()
