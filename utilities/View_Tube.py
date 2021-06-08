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
                    

#######################################
#####      Button Code         ########
#######################################    
def handle_enter(event):
    entry_barcode.config({"background": "White"})

    status = True
    if entry_barcode.get() == '':
        entry_barcode.config({"background": "Red"})
        text_entryStatus.delete("1.0", tk.END)
        text_entryStatus.insert("1.0", "Enter a tube")
        status = False

    if status:         
        barcode = entry_barcode.get()
        database = db.db()
        tube2 = database.get_tube(barcode)
        textTube = str(tube2)
        entry_barcode.delete(0, tk.END)
        text_entryStatus.delete("1.0", tk.END)
        text_entryStatus.insert("1.0", textTube)

window = tk.Tk()
window.title("View Tube GUI")
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

label_barcode = tk.Label(master=frame_entry, text="Barcode")
entry_barcode = tk.Entry(master=frame_entry)

button = tk.Button(
    master=frame_entry,
    text="Look up tube",
    width=33,
    height=2,
    bg="blue",
    fg="yellow",
)
button.bind("<Button-1>", handle_enter)
text_entryStatus = tk.Text(master=frame_entry, width=50, height=40)

############  Pack Everything Together  ##########
entry = tk.Entry()

label_barcode.pack()
entry_barcode.pack()

button.pack()
text_entryStatus.pack()


# Execute mainloop
window.mainloop()
