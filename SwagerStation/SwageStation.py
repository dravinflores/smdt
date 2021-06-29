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
path=os.path.dirname(os.path.abspath(__file__))

# This is a constant
NoneValueFloat: float = 3.0E8


def write(code, lengths, cleanCode, name):
    database = db.db()
    tube1 = tube.Tube()
    tube1.set_ID(code)

    raw = float(lengths[0])
    swage_len = float(lengths[1])
    clean = cleanCode
    username = name

    if swage_len > 299792458.00:
        raw = None

    tube1.swage.add_record(
        swage.SwageRecord(
            raw_length=raw, 
            swage_length=swage_len, 
            clean_code=clean, 
            user=username
        )
    )
    database.add_tube(tube1)
                    

#######################################
#####      Swage Entry Code    ########
#######################################    
def handle_enter(event):
    entry_name.config({"background": "White"})
    entry_barcode.config({"background": "White"})
    entry_length.config({"background": "White"})
    entry_slength.config({"background": "White"})

    status = True
    using_default_swage_length_value = False

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

    # For the database as it is currently, we would really like ignore the 
    # swage length, because we are tensioning the tube before we swage. So 
    # we want to edit this part.
    if entry_slength.get() == '':
        entry_slength.config({"background": "Red"})
        text_entryStatus.delete("1.0", tk.END)
        # text_entryStatus.insert("1.0", "Fill in all fields")
        text_entryStatus.insert("1.0", "Using a default value.")
        status = True
        using_default_swage_length_value = True

    if status:         
        name = entry_name.get()
        barcode = entry_barcode.get()
        firstLength = entry_length.get()

        if using_default_swage_length_value:
            secondLength = NoneValueFloat
        else:
            secondLength = entry_slength.get()

        write(
            barcode, 
            [firstLength,secondLength], 
            sv_cleanCode.get(),
            name
        )

        entry_barcode.delete(0, tk.END)
        entry_length.delete(0, tk.END)
        entry_slength.delete(0, tk.END)
        sv_cleanCode.set("3: Only Vacuumed")
        text_entryStatus.delete("1.0", tk.END)
        text_entryStatus.insert("1.0", barcode + " was entered\ninto database")
            

filename = os.path.join(
    path,
    "SwagerData",
    f"{datetime.now().strftime('%m.%d.%Y_%H_%M_%S.csv')}"
)

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
frame_entry.pack()

########### Entry Frame ###############
label_name = tk.Label(master=frame_entry, text="Name")
entry_name = tk.Entry(master=frame_entry)

label_barcode = tk.Label(master=frame_entry, text="Barcode")

entry_barcode = tk.Entry(master=frame_entry)

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

button.pack()
text_entryStatus.pack()

# Execute mainloop
window.mainloop()
