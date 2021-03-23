# -*- coding: utf-8 -*-

'''
Bentness GUI

Description: This simply records the bentness of the tube. It puts it in the
directory called "BentnessData". It is a simple csv file that is created
where the name, time, bentness and code is recorded. 

To run, first install Tkinter and pickle modules into your python library. After
that, running is as simple as: python "Bentness GUI.py" or double clicking in 
Windows 10. 

@author: Jason Gombas
'''

import tkinter as tk
from tkinter import StringVar
import os
from datetime import datetime

path = os.getcwd() 

def write(code, length, name):
    try:
        comment = text_comment.get('1.0',tk.END)[0:-1]
        comment = comment.replace(',',':')
        comment = comment.replace('\n','. ')
        with open(filename, 'r') as ff:
            lines = list(filter(lambda x: x != '\n', ff.readlines()))
            lines.append(f"{code},{length},\
{datetime.now().strftime('%m.%d.%Y_%H_%M_%S')},{name},{comment}\n")
        open(filename,'w').writelines(lines)
        
    except FileNotFoundError:
        open(filename,'w').close()
        write(code, length, name)

#######################################
#####      Swage Entry Code    ########
#######################################    
def handle_enter(event):
    entry_name.config({"background": "White"})
    entry_barcode.config({"background": "White"})
    entry_length.config({"background": "White"})

    if button.cget("text") == "Create Entry":
        status = True
        if not entry_length.get().replace('.', '', 1).replace('-', '', 1).isdigit():
            entry_length.config({"background": "Red"})
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
        if status:         
            name = entry_name.get()
            barcode = entry_barcode.get()
            firstLength = entry_length.get()
            write(barcode,firstLength,name)
            entry_barcode.delete(0, tk.END)
            entry_length.delete(0, tk.END)
            text_comment.delete("1.0", tk.END)
            
filename = "BentnessData\\" + f"{datetime.now().strftime('%m.%d.%Y_%H_%M_%S.csv')}"
window = tk.Tk()
window.title("Bentness GUI")
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

label_length = tk.Label(master=frame_entry, text='Gap Size')
entry_length = tk.Entry(master=frame_entry)

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


############  Pack Everything Together  ##########
entry = tk.Entry()
label_name.pack()
entry_name.pack()

label_barcode.pack()
entry_barcode.pack()

label_length.pack()
entry_length.pack()

label_comment.pack()
text_comment.pack()

button.pack()

# Execute mainloop
window.mainloop()
