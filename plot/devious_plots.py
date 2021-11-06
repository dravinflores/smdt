###############################################################################
#   File: devious_plots.py
#   Author(s):  Paul Johnecheck
#   Date Created: 5 October, 2021
#
#   Purpose: Uses matplotlib to create several plots related to tension.
#
###############################################################################
from typing import List, Any

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta
import numpy as np
import sys

dropbox_dir = r'C:\Users\Third\Dropbox\sMDT'
sys.path.append(dropbox_dir)

from sMDT.db import db


#If True, the code will remove outliers outside of the following values
REMOVE_OUTLIERS = True
RAW_MIN = -12
RAW_MAX = -8
SWAGE_MIN = -2
SWAGE_MAX = 2
TENSION_MIN = 200
TENSION_MAX = 500
LEAK_MIN = 0
LEAK_MAX = 100000
DARK_MIN = 0
DARK_MAX = 100000

def get_tension1(tube, min_date):
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    swage_length_rec = None
    try:  # gets the first SwageRecord with a value for swage_length
        swage_length_rec = next(rec for rec in swage_records if rec.swage_length and rec.date.date() > min_date)
    except StopIteration:
        # tube has no swage length recorded
        pass
    if swage_length_rec:  # only consider the tensions if the tube has been swaged
        # sort tension records by date
        tension_records = sorted(tube.tension.m_records, key=lambda rec: rec.date)
        pre_tension_rec = None
        try:  # gets the last TensionRecord before the tube was swaged
            generator = (rec for rec in tension_records if rec.date < swage_length_rec.date)
            while True:
                pre_tension_rec = next(generator)
        except StopIteration:
            # we hit this exception after we run out of tension records before swaging,
            # meaning pre_tension record is now the last record before swaging
                return (pre_tension_rec.tension, pre_tension_rec.date) if pre_tension_rec else None

def get_tension2(tube, min_date):
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    swage_length_rec = None
    try:  # gets the first SwageRecord with a value for swage_length
        swage_length_rec = next(rec for rec in swage_records if rec.swage_length and rec.date.date() > min_date)
    except StopIteration:
        # tube has no swage length recorded
        pass
    if swage_length_rec:  # only consider the tensions if the tube has been swaged
        # sort tension records by date
        tension_records = sorted(tube.tension.m_records, key=lambda rec: rec.date)
        try:  # gets the first TensionRecord after the tube was swaged
            post_tension_rec = next(rec for rec in tension_records if rec.date > swage_length_rec.date)
            return (post_tension_rec.tension, post_tension_rec.date)
        except StopIteration:
            pass

def get_raw_length(tube, min_date):
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    try:  # gets the first SwageRecord with a value for raw_length
        raw_length_rec = next(rec for rec in swage_records if rec.raw_length and rec.date.date() > min_date)
        return (raw_length_rec.raw_length, raw_length_rec.date)
    except StopIteration:
        pass

def get_swage_length(tube, min_date):
    swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)
    try:  # gets the first SwageRecord with a value for swage_length
        swage_length_rec = next(rec for rec in swage_records if rec.swage_length and rec.date.date() > min_date)
        return (swage_length_rec.swage_length, swage_length_rec.date)
    except StopIteration:
        pass

def get_length_diffs(tube, min_date):
    try:
        swage_length, date = get_swage_length(tube, min_date)
        raw_length = get_raw_length(tube, min_date)[0]
        return (swage_length - raw_length, date)
    except TypeError:
        return None

def get_tension_diffs(tube, min_date):
    try:
        tension1, date = get_tension1(tube, min_date)
        tension2 = get_tension2(tube, min_date)[0]
        return (tension2 - tension1, date)
    except TypeError:
        return None

def get_leak(tube, min_date):
    leak_records = sorted([record for record in tube.leak.m_records if record.date], key=lambda rec: rec.date)
    try:  # gets the first SwageRecord with a value for swage_length
        leak_rec = next(rec for rec in leak_records if rec.leak_rate and rec.date.date() > min_date)
        return (leak_rec.leak_rate, leak_rec.date)

    except StopIteration:
        # tube has no swage length recorded
        pass

def get_dark_current(tube, min_date):
    dark_records = sorted([record for record in tube.dark_current.m_records if record.date], key=lambda rec: rec.date)
    try:  # gets the first SwageRecord with a value for swage_length
        dark_rec = next(rec for rec in dark_records if rec.dark_current and rec.date.date() > min_date)
        return (dark_rec.dark_current, dark_rec.date)
    except StopIteration:
        # tube has no swage length recorded
        pass


class Plotter:
    def __init__(self, num_days, remove_outliers=False, outlier_stdev=2):
        database = db()
        self.tubes = database.get_tubes()
        self.plots = []
        self.num_days = num_days
        self.min_date = date.today() - timedelta(days=num_days)
        self.dates = [self.min_date + timedelta(days=(n+1)) for n in range(num_days)]
        self.remove_outliers = remove_outliers
        self.outlier_stdev = 2

    def add_plot(self, plot_tup, f):
        self.plots.append((plot_tup, f))

    def plot(self):
        nrows = int(np.ceil(len(self.plots)/2))
        ncol = 2
        fig, axs = plt.subplots(nrows, 2)
        fig.tight_layout()
        for i,plot in enumerate(self.plots):
            self.plots[i] = (plot[0], [plot[1](tube, self.min_date) for tube in self.tubes if plot[1](tube, self.min_date)])
        for i,ax in enumerate(axs.flat):
                (title, x_label, y_label), data_tups = self.plots[i]
                data_by_date = [[] for i in range(self.num_days)]
                [data_by_date[(date.date() - self.min_date).days - 1].append(data) for data, date in data_tups if date.date() > self.min_date]
                data_avg_by_date = [sum(date_list) / len(date_list) if date_list else np.nan for date_list in data_by_date]
                data_stdev_by_date = [np.std(date_list) if date_list else np.nan for date_list in data_by_date]
                data_median_by_date = [np.median(date_list) if date_list else np.nan for date_list in data_by_date]

                if self.remove_outliers:
                    all_data = []
                    [all_data.extend([data for data in date_list if not np.isnan(data)]) for date_list in data_by_date]
                    total_mean = sum(all_data)/len(all_data)
                    total_stdev = np.std([data for data, date in data_tups if date.date() > self.min_date])
                    data_by_date = [[data for data in date_list if np.abs(data - total_mean) < total_stdev * self.outlier_stdev] for date_list in data_by_date]

                    #recalculate values to plot with outliers removed
                    data_avg_by_date = [sum(date_list) / len(date_list) if date_list else np.nan for date_list in data_by_date]
                    data_stdev_by_date = [np.std(date_list) if date_list else np.nan for date_list in data_by_date]
                    data_median_by_date = [np.median(date_list) if date_list else np.nan for date_list in data_by_date]



                ax.errorbar(self.dates, data_avg_by_date, yerr=data_stdev_by_date, fmt="o")
                ax.scatter(self.dates, data_median_by_date, c='r', marker='x')
                ax.set_title(title)
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.set_xticks(self.dates[::7])
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
                ax.grid()

        plt.show()



if __name__ == '__main__':

    #past N days
    NUM_DAYS = 120

    REMOVE_OUTLIERS = True
    #a data point is an outlier if it is greater than N standard deviations from the mean of medians.
    N_STDEV = 4


    plotter = Plotter(NUM_DAYS, REMOVE_OUTLIERS, N_STDEV)
    plotter.add_plot(("Raw Length Average by Day", "Date, Past 60 Days", "Raw Length (mm)"), get_raw_length)
    plotter.add_plot(("Pre-Swage Tension Average by Day", "Date, Past 60 Days", "Tension (g)"), get_tension1)
    plotter.add_plot(("Swage Length Average by Day", "Date, Past 60 Days", "Raw Length (mm)"), get_swage_length)
    plotter.add_plot(("Post-Swage Tension Average by Day", "Date, Past 60 Days", "Tension (g)"), get_tension2)
    plotter.add_plot(("Difference between Raw and Swage Length Average by Day", "Date, Past 60 Days", "Lenth Difference (mm)"), get_length_diffs)
    plotter.add_plot(("Difference between Pre and Post Swage Tension Average by Day", "Date, Past 60 Days", "Tension Difference (g)"), get_length_diffs)
    plotter.add_plot(("Leak Rate Average by Day", "Date, Past 60 Days", "Leak Rate (mbar l/s)"), get_leak)
    plotter.add_plot(("Dark Current Average by Day", "Date, Past 60 Days", "Leak Rate (nA)"), get_dark_current)
    plotter.plot()


    plt.show()