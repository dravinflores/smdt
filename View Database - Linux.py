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
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandas import DataFrame
from collections import Counter
import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from tkinter import StringVar
import pickle
import os
from datetime import datetime
import numpy as np
import synchronize as sy

path = os.getcwd() 
#sy.synchronize()

def loadDatabase():
    return pickle.load(open(os.path.abspath(os.path.join(path, os.pardir))\
                            +'/sMDT/database.p', 'rb'))

##################################################################################
# Update All Tube Data function
##################################################################################    
def OnSearching(sv):
    code = sv.get()
    database = loadDatabase()
    swageText.config(state='normal')
    tensionText.config(state='normal')
    leakText.config(state='normal')
    darkText.config(state='normal')
    swageText.delete("1.0", tk.END)
    tensionText.delete("1.0", tk.END)
    leakText.delete("1.0", tk.END)
    darkText.delete("1.0", tk.END)       
    if code == '':
        swageText.config(state='disabled')
        tensionText.config(state='disabled')
        leakText.config(state='disabled')
        darkText.config(state='disabled')
    else:
        if code in database.keys():
            # Swager
            if 'swagerUser' in database[code].keys():
                printString='First Swager User:'
                printString+= database[code]['swagerUser'][0]
                printString+='Date Swaged:'
                printString+=database[code]['swagerDate'][0]+'\n'
                printString+='Error Codes:\n'
                for errorCode in database[code]['eCode']:
                    if errorCode[0] != '0': 
                        printString+=errorCode + '\n'
                printString+='Clean Codes:\n'
                for cleanCode in database[code]['cCode']:
                     printString+=cleanCode + '\n'
                printString+="Comments:\n"
                for comment in database[code]['swagerComment']:
                    printString+=comment + '\n'
                printString+='\nSWAGER FILES\n'
                for file in database[code]['swagerFile']:
                    printString+=file + '\n'
                printString += '\n'
                
                if 'good' in database[code].keys():
                    if database[code].get('good') != True: 
                        printString+='Errors listed below\n'
                if 'failsSwager' in database[code].keys() and database[code]['failsSwager']==True:
                    printString+='Tube failed swaging\n'
                for error in database[code]['eCode']: 
                    if error[0] != '0':
                        printString+=error + '\n'
                if 'failsFirstTension' in database[code].keys() and database[code]['failsFirstTension']==True:
                    printString+='Tube failed first tension\n'
                elif 'failsLeak' in database[code].keys() and database[code]['failsLeak']==True:
                    printString+='Tube failed leak test\n'
                elif 'failsCurrent' in database[code].keys() and database[code]['failsCurrent']==True:
                    printString+='Tube failed dark current test\n'
                elif 'failsSecondTension' in database[code].keys() and database[code]['failsSecondTension']==True:
                    printString+='Tube failed second tension test\n'
                swageText.insert("1.0",printString)
            else:
                swageText.insert("1.0","No Information Available")
                
            # Leak Rate
            if 'leakUser' in database[code].keys():
                printString = ''
                for number, leakRate in enumerate(database[code]['leakRate']):
                    printString+= "User: " + database[code]['leakUser'][number] + \
                               "\nRate: " + str(leakRate) + '\n' +\
                               "Date: " + str(database[code]['leakDateTime'][number]+\
                                "\n\n")
                printString+='\nLEAK FILES\n'
                for file in database[code]['leakFile']:
                    printString+=file + '\n'    
                leakText.insert("1.0",printString)
            else: leakText.insert("1.0","No Information Available")
            
            # Tension
            if 'tensionUser' in database[code].keys():
                printString = 'First Tensions:\n'
                for number, firstTension in enumerate(database[code]['firstTensions']):
                    printString+=database[code]['firstTensionUsers'][number] + ': '\
                            + str(firstTension) \
                            + '\t\t' + str(database[code]['firstTensionDates'][number] + '\n')
                printString+='\nSecond Tensions:\n'
                for number, secondTension in enumerate(database[code]['secondTensions']):
                    printString+=database[code]['secondTensionUsers'][number] + ': '\
                            + str(secondTension) \
                            + '\t\t' + str(database[code]['secondTensionDates'][number] + '\n') 
                printString+='\nAll Tensions:\n'
                for number, user in enumerate(database[code]['tensionUser']):
                    printString+= user + ': '\
                            + str(database[code]['tensions'][number]) \
                            + '\t\t' + str(database[code]['tensionDateTime'][number] + '\n')                           
                printString+='\n\n TENSION FILES\n'
                for file in database[code]['tensionFile']:
                    printString+=file + '\n'
                tensionText.insert("1.0",printString)
            else: tensionText.insert('1.0','No Information Available\n')
            
            # Dark Current
            if 'currentFile' in database[code].keys():
                printString='Dark Current' + '\t\t' + 'Test Date\n' 
                for number, current in enumerate(database[code]['darkCurrents']):
                    printString+= current + '\t\t' + database[code]['currentTestDates'][number]

                printString+='\nDARK CURRENT FILE\n'
                printString+=database[code]['currentFile'] + '\n'  
                darkText.insert('1.0', printString)
            else:
                darkText.insert('1.0','No Information Available')
                    
        
        else:
            swageText.insert("1.0","Not in Database")
        
        swageText.config(state='disabled')
        tensionText.config(state='disabled')
        leakText.config(state='disabled')
        darkText.config(state='disabled') 
        
##################################################################################
# Update Plots Function
##################################################################################
def updatePlots(data): #data is [tension1, tension2, diff tension, leak, current, errors]
    global axes
    global bar1
    tenDF = DataFrame([-1])
    if data[0] != []: 
        tenDF = DataFrame(data[0])
    axes[0].clear()      
    axes[0] = figure.add_subplot(231)
    tenDF.plot(kind='hist', legend=False, ax=axes[0])
    axes[0].set_title('First Tension')  

    tenDF2 = DataFrame([-1])
    if data[1] != []: 
        tenDF2 = DataFrame(data[1])    
    axes[1].clear()    
    axes[1] = figure.add_subplot(232)
    tenDF2.plot(kind='hist', legend=False, ax=axes[1])
    axes[1].set_title('Second Tension') 

    tendiffDF = DataFrame([-1])
    if data[2] != []:
        tendiffDF = DataFrame(data[2])
    axes[2].clear()    
    axes[2] = figure.add_subplot(233)
    tendiffDF.plot(kind='hist', legend=False, ax=axes[2])
    axes[2].set_title('Tension Difference') 

    leakDF = DataFrame([-1])
    if data[3] != []:
        leakDF = DataFrame(data[3])
    axes[3].clear()    
    axes[3] = figure.add_subplot(234)
    axes[3].set_xscale("log")
    leakDF.plot(kind='hist', bins=np.logspace(np.log10(0.0000000001),np.log10(0.0001), 50), legend=False, ax=axes[3])
    axes[3].set_title('Leak Rate') 

    currentDF = DataFrame([-1])
    if data[4] != []:
        currentDF = DataFrame(data[4])
    axes[4].clear()    
    axes[4] = figure.add_subplot(235)
    currentDF.plot(kind='hist', legend=False, ax=axes[4])
    axes[4].set_title('Dark Current') 

    letter_counts = Counter([-1])
    if data[5] != []:
        letter_counts = Counter(data[5])
    df2 = DataFrame.from_dict(letter_counts,orient='index')
    axes[5].clear()    
    axes[5] = figure.add_subplot(236)
    df2.plot(kind='bar', legend=False, ax=axes[5])
    axes[5].set_title('Error Codes') 
    
    bar1.draw()


##################################################################################
# Update Treeview Function
##################################################################################
def updateTreeView(event):
    database = sy.synchronize()
    tree.delete(*tree.get_children())
    for tube, tubeData in sorted(database.items(), reverse=True):
        if not tube or 'swagerUser' not in tubeData.keys(): continue
        
        swagerUser = tubeData.get("swagerUser")[0]
        swagerDate = tubeData.get("swagerDate")[0]
        dateParts = swagerDate.split('.')
        if len(dateParts)==3: swagerDate = '{1}.{0}.{2}'.format(dateParts[0],dateParts[1],dateParts[2])
        else: swagerDate = swagerDate = tubeData.get("swagerDate")[0]
        status = 'uncertain'
        if 'good' in tubeData.keys():
            if tubeData.get('good') == True: status = 'good'
            else: status = 'bad'
        tension1Date = tubeData.get('firstTensionDate')
        tension2Date = tubeData.get('secondTensionDate')
        if 'firstTension' in tubeData.keys():
            tension1 = '{0:.3g}'.format(tubeData.get('firstTension'))
        else: tension1 = 'None'
        if 'secondTension' in tubeData.keys():
            tension2 = '{0:.3g}'.format(tubeData.get('secondTension'))
        else: tension2 = 'None'
        if 'leakRate' in tubeData.keys() and tubeData.get('leakRate')!=[]: leakRate = "{0:.2g}".format(min(tubeData.get('leakRate')))
        else: leakRate = "None"
        darkCurrent = "None"
        if 'darkCurrents' in tubeData.keys() and tubeData.get('darkCurrents') != []:
            darkCurrent =  database[tube]['darkCurrents'][-1]
        rawLength = 'None'
        swageLength = 'None'
        if 'rawLength' in tubeData.keys() and tubeData.get('rawLength')[0]!='': 
            rawLength = 1624.3 + float(tubeData.get('rawLength')[0])
            rawLength = '{0:.6g}'.format(rawLength)
        if 'swageLength' in tubeData.keys() and tubeData.get('swageLength')[0]!='': 
            swageLength = 1624.3 + float(tubeData.get('swageLength')[0])
            swageLength = '{0:.6g}'.format(swageLength)
        tree.insert("", 'end', tube, text=tube,\
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
    
    tree.bind("<Double-1>", OnDoubleClick)
    tree.pack(side="right",fill="both", expand=True)   

##################################################################################
# Get Data for plotting tab
##################################################################################
def getData(minTube, maxTube):
    first_tensions = []
    second_tensions = []
    diff_tensions = []
    leak_rates = []
    final_currents = []
    error_codes = []
    for tube,tubeData in database.items():
        if tube > minTube and tube < maxTube:
            if 'firstTension' in tubeData.keys():
                first_tensions.append(float(tubeData.get('firstTension')))
            if 'secondTension' in tubeData.keys():
                second_tensions.append(float(tubeData.get('secondTension')))
                diff_tensions.append(float(tubeData.get('secondTension') \
                                         - tubeData.get('firstTension')))
            if 'leakRate' in tubeData.keys() and tubeData.get('leakRate') != []:
                leak_rates.append(float(tubeData.get('leakRate')[-1]))
            if 'darkCurrents' in tubeData.keys() and tubeData.get('darkCurrents') != []:
                final_currents.append(float(tubeData.get('darkCurrents')[-1]))
            if 'eCode' in tubeData.keys():
                for code in tubeData.get('eCode'):
                    if code != 'Unknown' and code[0] != '0':
                        error_codes.append(code[0:8])
    return [first_tensions,second_tensions,diff_tensions,leak_rates,final_currents,error_codes]

# Handle for updating plots button
def handleUpdatePlots(event):
    minTubeNumber = minTubeEntry.get()
    maxTubeNumber = maxTubeEntry.get()
    data = getData(minTubeNumber, maxTubeNumber)
    updatePlots(data)

# Handle for double clicking row in overview tab
def OnDoubleClick(event):
    tube = tree.selection()[0]
    nb.select(f2)
    tubeEntry.delete(0, tk.END)
    tubeEntry.insert(0,tube)


##################################################################################
# Main Function that sets up all visuals
##################################################################################
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Database Viewer")
    nb= ttk.Notebook(master=root)
    nb.pack(fill='both',expand=True)

    s=ttk.Style()
    #s.map('Treeview', foreground=fixed_map('foreground'),
    #          background=fixed_map('background'))
    #s.theme_use('winnative')
    s.configure('Treeview', rowheight=22)


    f1 = tk.Frame(nb) 
    nb.add(f1,text='Overview')
    f2=tk.Frame(nb)
    nb.add(f2,text='All Tube Data')
    f3=tk.Frame(nb)
    nb.add(f3,text='Graphs')

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
    
    database = loadDatabase()
    updateTreeView(database)

    
    #######################################################################
    ## All Tube Data Page
    searchFrame = tk.Frame(master=f2)
    
    searchFrame.grid(row=0,column=0)
    sv_barcode = StringVar()
    sv_barcode.trace("w", lambda name, index, mode, 
                sv_barcode=sv_barcode: OnSearching(sv_barcode))
    tubeLabel = tk.Label(master=searchFrame, text="Barcode")
    tubeEntry = tk.Entry(master=searchFrame, textvariable=sv_barcode)
    tubeLabel.pack(side='left')
    tubeEntry.pack(side='left')
    
    tk.Label(master=f2, text="Swage Data").grid(row=1,column=0)
    swageText = tk.Text(master=f2,width=70,height=28)
    swageText.grid(row=2,column=0)
    
    tk.Label(master=f2, text='Tension Data').grid(row=3,column=0)
    tensionText = tk.Text(master=f2,width=70,height=28)
    tensionText.grid(row=4,column=0)
    
    tk.Label(master=f2, text='Leak Data').grid(row=1,column=1)
    leakText = tk.Text(master=f2,width=70,height=28)
    leakText.grid(row=2,column=1)
    
    tk.Label(master=f2,text='Dark Current Data').grid(row=3,column=1)
    darkText = tk.Text(master=f2,width=70,height=28)
    darkText.grid(row=4,column=1)
    
    swageText.config(state='disabled')
    tensionText.config(state='disabled')
    leakText.config(state='disabled')
    darkText.config(state='disabled')


    #########################################################################
    ## Graphs Page
    
    ## Initialize graphs with default plots
    figure = plt.Figure(figsize=(10,9), dpi=100)
    
    maxtubenumber = sorted(database.items(), reverse=True)[0][0]
    data = getData('MSU00500', maxtubenumber)
    
    tenDF = DataFrame(data[0])        
    ax1 = figure.add_subplot(231)
    tenDF.plot(kind='hist', bins=20, legend=False, ax=ax1)
    ax1.set_title('First Tension')  

    tenDF2 = DataFrame(data[1])        
    ax2 = figure.add_subplot(232)
    tenDF2.plot(kind='hist', bins=20, legend=False, ax=ax2)
    ax2.set_title('Second Tension') 

    tendiffDF = DataFrame(data[2])
    ax3 = figure.add_subplot(233)
    tendiffDF.plot(kind='hist', bins=20, legend=False, ax=ax3)
    ax3.set_title('Tension Difference') 

    leakDF = DataFrame(data[3])
    ax4 = figure.add_subplot(234)
    ax4.set_xscale("log")
    leakDF.plot(kind='hist', bins=np.logspace(np.log10(0.0000000001),np.log10(0.0001), 50), \
                legend=False, ax=ax4)
    ax4.set_title('Leak Rate') 

    currentDF = DataFrame(data[4])
    ax5 = figure.add_subplot(235)
    currentDF.plot(kind='hist', bins=20, legend=False, ax=ax5)
    ax5.set_title('Dark Current') 

    letter_counts = Counter(data[5])
    df2 = DataFrame.from_dict(letter_counts,orient='index')
    ax6 = figure.add_subplot(236)
    df2.plot(kind='bar', legend=False, ax=ax6)
    ax6.set_title('Error Codes') 
    
    bar1 = FigureCanvasTkAgg(figure, f3)
    bar1.get_tk_widget().pack(side='top', fill='both', expand=True)

    axes = [ax1,ax2,ax3,ax4,ax5,ax6]

    controlFrame = tk.Frame(f3)
    maxTubeEntry = tk.Entry(master=controlFrame)
    minTubeEntry = tk.Entry(master=controlFrame)
    updatePlotsButton = tk.Button(
            master=f3,
            text="Update Plots",
            bg="blue",
            fg="yellow",
            )
    updatePlotsButton.bind("<Button-1>", handleUpdatePlots)
    minLabel = tk.Label(master=controlFrame, text='Min Tube')
    maxLabel = tk.Label(master=controlFrame, text='Max Tube')
    maxtubenumber = "("+maxtubenumber+")"
    maxTubeNumberLabel = tk.Label(master=controlFrame, text = maxtubenumber)
    
    minLabel.pack(side='left')
    minTubeEntry.pack(side='left')
    maxLabel.pack(side='left')
    maxTubeEntry.pack(side='left')
    maxTubeNumberLabel.pack(side='left')
    updatePlotsButton.pack(side='left')
    
    controlFrame.pack(side='top', fill='both', expand=True)
    nb.enable_traversal()
    root.wm_geometry("1200x1000")
    root.mainloop()




