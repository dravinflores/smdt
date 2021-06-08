# -*- coding: utf-8 -*-

'''
View Database GUI
Created on Thursday August 14, 2020

Description: This code essentially makes the database stored in a pickle
file visible to a user.

To run, first instal Tkinter and pickle modules into your python library. After
that, running is as simple as: python "View Database.py" or double clicking in 
Windows 10. 

@author: Jason Gombas
'''

################################################################################
#
# This file merges both the Linux and Windows versions of the programs in an 
# effort to consolidate the main program. A function is provided to get which
# OS the program is running on.
#
################################################################################

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas import DataFrame
from collections import Counter
import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import StringVar
import sys
import os
from datetime import datetime
import numpy as np
import platform

DROPBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DROPBOX_DIR)
from sMDT import db, tube
from sMDT.data import swage
from sMDT.data.status import Status


# Global Variables.
path = os.getcwd()

def getHostOS():
    """Returns: 'Windows', 'Linux', or 'Darwin'"""
    return platform.system()


################################################################################
# Update Treeview Function
################################################################################
def updateTreeView(event):
    datab = db.db()
    listofIDs = datab.get_IDs()
    tree.delete(*tree.get_children())
    for barcode in sorted(listofIDs, reverse=True):
        tube = datab.get_tube(barcode)
        try:
            swagerUser = tube.swage.get_record(mode='first').user
            swagerDate = tube.swage.get_record(mode='first').date
            tension1Date = tube.tension.get_record(mode='first').date
            tension2Date = tube.tension.get_record().date
            tension1 = tube.tension.get_record(mode='first').tension
            tension2 = tube.tension.get_record().tension
            leakRate = tube.leak.get_record().leak_rate
            darkCurrent =  tube.dark_current.get_record().dark_current
            rawLength = 1624.3 + float(tube.swage.get_record().raw_length)
            rawLength = '{0:.6g}'.format(rawLength)
            swageLength = 1624.3 + float(tube.swage.get_record().swage_length)
            swageLength = '{0:.6g}'.format(swageLength)
            status = tube.status()
        except IndexError:
            continue
        except TypeError:
            continue

        if status == Status.PASS:
            status = 'good'
        elif status == Status.FAIL:
            status = 'bad'
        elif status == Status.INCOMPLETE:
            status = 'uncertain'
        tree.insert("", 'end', barcode, text=barcode,\
        values=(swagerUser,\
            str(swagerDate),\
                str(tension1Date),\
                    str(tension1),\
                        str(tension2Date),\
                            str(tension2),\
                                str(leakRate),\
                                    darkCurrent,\
                                        rawLength,\
                                            swageLength),\
            tags = (str(status),))
        
    tree.tag_configure('bad', background='#ffcccb')
    tree.tag_configure('good', background='#008000')
    tree.tag_configure('uncertain', background='#FFFF00')
    tree.pack(side="right",fill="both", expand=True)   


################################################################################
# Main Function that sets up all visuals
################################################################################
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Database Viewer")
    nb= ttk.Notebook(master=root)
    nb.pack(fill='both',expand=True)

    s=ttk.Style()
    print('Configuring')
    s.configure('Treeview', rowheight=22)


    f1 = tk.Frame(nb) 
    nb.add(f1,text='Overview')
    print('Adding button')
    updateTreeViewButton = tk.Button(
            master=nb,
            text="Update Database",
            bg="blue",
            fg="yellow",
            )
    updateTreeViewButton.bind("<Button-1>", updateTreeView)
    updateTreeViewButton.pack(side='top')
    nb.select(f1)
    
    ###################################################################
    ## Overview Page
    print('Putting together treeview')
    tree=ttk.Treeview(master=f1)
    tree["columns"]=("two","twopfive","three", "four", "five", \
                        "six", "seven", "eight", "nine", "ten")
    
    tree.column("#0", width=80, minwidth=80, stretch=tk.NO)
    tree.column("two", width=80, minwidth=80, stretch=tk.NO)
    tree.column("twopfive", width=150, minwidth=80,stretch=tk.NO)
    tree.column("three", width=150, minwidth=50, stretch=tk.NO)
    tree.column("four", width=60, minwidth=50, stretch=tk.NO)
    tree.column("five", width=150, minwidth=50, stretch=tk.NO)
    tree.column("six", width=60, minwidth=50, stretch=tk.NO)
    tree.column("seven", width=80, minwidth=50, stretch=tk.NO)
    tree.column("eight", width=100, minwidth=50, stretch=tk.NO)
    tree.column("nine", width=80, minwidth=50, stretch=tk.NO)
    tree.column("ten", width=80, minwidth=50, stretch=tk.NO)
    
    tree.heading("#0",text="Tube ID",anchor=tk.W)
    tree.heading("two", text="Swage User",anchor=tk.W)
    tree.heading("twopfive", text="Swage Date", anchor=tk.W)
    tree.heading("three", text="Tens. 1 Date",anchor=tk.W)
    tree.heading("four", text="Tension 1",anchor=tk.W)
    tree.heading("five", text="Tens. 2 Date",anchor=tk.W)
    tree.heading("six", text="Tension 2",anchor=tk.W)
    tree.heading("seven", text="Leak Rate",anchor=tk.W)
    tree.heading("eight", text="Dark Current",anchor=tk.W)
    tree.heading("nine", text="Raw Length",anchor=tk.W)
    tree.heading("ten", text="Swage Length",anchor=tk.W)
    print('Updating tree view')
    updateTreeView(None)
    print('done with updating')
    
    nb.enable_traversal()
    print('setting up geometry')
    root.wm_geometry("1200x1000")
    print('entering main loop')
    root.mainloop()