###############################################################################
#   File: tension_plots.py
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


if __name__ == '__main__':

    database = db()
    tubes = database.get_tubes()

    # all these are lists of tuples, (value, date)
    tensions1 = []
    tensions2 = []
    raw_lengths = []
    swage_lengths = []
    length_diffs = []
    tension_diffs = []
    leaks = []
    dark_currents = []


    min_date = date.today() - timedelta(days=60)

    for tube in tubes:

        # sort swage records by date, remove records with no date
        swage_records = sorted([record for record in tube.swage.m_records if record.date], key=lambda rec: rec.date)

        swage_length_rec = None
        try:  # gets the first SwageRecord with a value for swage_length
            swage_length_rec = next(rec for rec in swage_records if rec.swage_length and rec.date.date() > min_date)

            # remove outliers
            if SWAGE_MIN < swage_length_rec.swage_length < SWAGE_MAX or not REMOVE_OUTLIERS:
                swage_lengths.append((swage_length_rec.swage_length, swage_length_rec.date))

        except StopIteration:
            # tube has no swage length recorded
            pass

        try:  # gets the first SwageRecord with a value for raw_length
            raw_length_rec = next(rec for rec in swage_records if rec.raw_length and rec.date.date() > min_date)

            # remove outliers
            if RAW_MIN < raw_length_rec.raw_length < RAW_MAX or not REMOVE_OUTLIERS:
                raw_lengths.append((raw_length_rec.raw_length, raw_length_rec.date))

        except StopIteration:
            # tube has no raw length recorded
            pass

        if swage_length_rec:  # only consider the tensions if the tube has been swaged

            # sort tension records by date
            tension_records = sorted(tube.tension.m_records, key=lambda rec: rec.date)

            try:  # gets the last TensionRecord before the tube was swaged
                generator = (rec for rec in tension_records if rec.date < swage_length_rec.date)
                while True:
                    pre_tension_rec = next(generator)

            except StopIteration:
                # we hit this exception after we run out of tension records before swaging,
                # meaning pre_tension record is now the last record before swaging
                # remove outliers
                if TENSION_MIN < pre_tension_rec.tension < TENSION_MAX or not REMOVE_OUTLIERS:
                    tensions1.append((pre_tension_rec.tension, pre_tension_rec.date))

            try:  # gets the first TensionRecord after the tube was swaged
                post_tension_rec = next(rec for rec in tension_records if rec.date > swage_length_rec.date)
                # remove outliers
                if TENSION_MIN < post_tension_rec.tension < TENSION_MAX or not REMOVE_OUTLIERS:
                    tensions2.append((post_tension_rec.tension, post_tension_rec.date))

            except StopIteration:
                # no tension record after swage
                pass

        if swage_length_rec and post_tension_rec:
            if SWAGE_MIN < swage_length_rec.swage_length < SWAGE_MAX and RAW_MIN < raw_length_rec.raw_length < RAW_MAX or not REMOVE_OUTLIERS:
                length_diffs.append((swage_length_rec.swage_length - raw_length_rec.raw_length, swage_length_rec.date))
            if TENSION_MIN < pre_tension_rec.tension < TENSION_MAX and TENSION_MIN < post_tension_rec.tension < TENSION_MAX or not REMOVE_OUTLIERS:
                tension_diffs.append((post_tension_rec.tension - pre_tension_rec.tension, swage_length_rec.date))

        leak_records = sorted([record for record in tube.leak.m_records if record.date], key=lambda rec: rec.date)
        try:  # gets the first SwageRecord with a value for swage_length
            leak_rec = next(rec for rec in leak_records if rec.leak_rate and rec.date.date() > min_date)

            # remove outliers
            if LEAK_MIN < leak_rec.leak_rate < LEAK_MAX or not REMOVE_OUTLIERS:
                leaks.append((leak_rec.leak_rate, leak_rec.date))

        except StopIteration:
            # tube has no swage length recorded
            pass

        dark_records = sorted([record for record in tube.dark_current.m_records if record.date], key=lambda rec: rec.date)
        try:  # gets the first SwageRecord with a value for swage_length
            dark_rec = next(rec for rec in dark_records if rec.dark_current and rec.date.date() > min_date)

            # remove outliers
            if DARK_MIN < dark_rec.dark_current < DARK_MAX or not REMOVE_OUTLIERS:
                dark_currents.append((dark_rec.dark_current, dark_rec.date))

        except StopIteration:
            # tube has no swage length recorded
            pass



    # all these are 2d lists each sublist represents a day., measurement_dates[0] is a list of measurements
    raw_len_dates = [[] for i in range(60)]
    swage_len_dates = [[] for i in range(60)]
    tension1_dates = [[] for i in range(60)]
    tension2_dates = [[] for i in range(60)]
    len_dif_dates = [[] for i in range(60)]
    tens_dif_dates = [[] for i in range(60)]
    dark_dates = [[] for i in range(60)]
    leak_dates = [[] for i in range(60)]

    #build the 2d array
    [raw_len_dates[(date.date()-min_date).days - 1].append(length) for length, date in raw_lengths if date.date() > min_date]
    #for length, date in raw_lengths: #equivalent code to the above line
    #    date_index = (date.date()-min_date).days - 1
    #    (raw_len_dates[date_index]).append(length)
    [swage_len_dates[(date.date() - min_date).days - 1].append(length) for length, date in swage_lengths if date.date() > min_date]
    [tension1_dates[(date.date() - min_date).days - 1].append(tension) for tension, date in tensions1 if date.date() > min_date]
    #for tension, date in tensions1: #equivalent code to the above line
    #    date_index = (date.date()-min_date).days - 1
    #    try:
    #        (tension1_dates[date_index]).append(tension)
    #    except IndexError:
    #        print(tension, date)
    [tension2_dates[(date.date() - min_date).days - 1].append(tension) for tension, date in tensions2 if date.date() > min_date]
    [len_dif_dates[(date.date() - min_date).days - 1].append(diff) for diff, date in length_diffs if date.date() > min_date]
    [tens_dif_dates[(date.date() - min_date).days - 1].append(diff) for diff, date in tension_diffs if date.date() > min_date]
    [dark_dates[(date.date() - min_date).days - 1].append(dark) for dark, date in dark_currents if date.date() > min_date]
    [leak_dates[(date.date() - min_date).days - 1].append(leak) for leak, date in leaks if date.date() > min_date]

    # calculate averages, "if date_list else np.nan" causes a point to be omitted if there is no data for that day
    # raw_len_avg = [] # Commented block is equivalent to the first line
    # for date_list in raw_len_dates:
    #    if date_list:
    #        date_max = max([length for length in date_list])
    #        date_sum = sum([length for length in date_list])
    #        date_len = len(date_list)
    #        raw_len_avg.append(date_sum/date_len)
    #    else:
    #        raw_len_avg.append(np.nan)
    raw_len_avg = [sum([length for length in date_list]) / len(date_list) if date_list else np.nan for date_list in raw_len_dates]
    swage_len_avg = [sum([length for length in date_list]) / len(date_list) if date_list else np.nan for date_list in swage_len_dates]
    tension1_avg = [sum([tension for tension in date_list]) / len(date_list) if date_list else np.nan for date_list in tension1_dates]
    tension2_avg = [sum([tension for tension in date_list]) / len(date_list) if date_list else np.nan for date_list in tension2_dates]
    len_dif_avg = [sum([diff for diff in date_list]) / len(date_list) if date_list else np.nan for date_list in len_dif_dates]
    tens_dif_avg = [sum([diff for diff in date_list]) / len(date_list) if date_list else np.nan for date_list in tens_dif_dates]
    dark_avg = [sum([dark for dark in date_list]) / len(date_list) if date_list else np.nan for date_list in dark_dates]
    leak_avg = [sum([leak for leak in date_list]) / len(date_list) if date_list else np.nan for date_list in leak_dates]

    # calculate standard deviations
    raw_len_stdev = [np.std(date_list) if date_list else np.nan for date_list in raw_len_dates]
    swage_len_stdev = [np.std(date_list) if date_list else np.nan for date_list in swage_len_dates]
    tension1_stdev = [np.std(date_list) if date_list else np.nan for date_list in tension1_dates]
    tension2_stdev = [np.std(date_list) if date_list else np.nan for date_list in tension2_dates]
    len_dif_stdev = [np.std(date_list) if date_list else np.nan for date_list in len_dif_dates]
    tens_dif_stdev = [np.std(date_list) if date_list else np.nan for date_list in tens_dif_dates]
    leak_stdev = [np.std(date_list) if date_list else np.nan for date_list in leak_dates]
    dark_stdev = [np.std(date_list) if date_list else np.nan for date_list in dark_dates]

    # plot
    dates = [min_date + timedelta(days=(n+1)) for n in range(60)]

    fig, ((raw_plot, tension1_plot), (swage_plot, tension2_plot), (len_dif_plot, tens_dif_plot), (dark_plot, leak_plot)) = plt.subplots(4,2)
    fig.tight_layout()

    raw_plot.errorbar(dates, raw_len_avg, yerr=raw_len_stdev, fmt="o")
    raw_plot.set_title("Raw Length Average by Day")
    raw_plot.set_xlabel("Date, Past 60 Days")
    raw_plot.set_ylabel("Raw Length (mm)")
    raw_plot.set_xticks(dates[::7])
    raw_plot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    raw_plot.grid()

    swage_plot.errorbar(dates, swage_len_avg, yerr=swage_len_stdev, fmt="o")
    swage_plot.set_title("Swage Length Average by Day")
    swage_plot.set_xlabel("Date, Past 60 Days")
    swage_plot.set_ylabel("Swage Length (mm)")
    swage_plot.set_xticks(dates[::7])
    swage_plot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    swage_plot.grid()

    tension1_plot.errorbar(dates, tension1_avg, yerr=tension1_stdev, fmt="o")
    tension1_plot.set_title("Pre-Swage Tension Average by Day")
    tension1_plot.set_xlabel("Date, Past 60 Days")
    tension1_plot.set_ylabel("Tension (g)")
    tension1_plot.set_xticks(dates[::7])
    tension1_plot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    tension1_plot.grid()

    tension2_plot.errorbar(dates, tension2_avg, yerr=tension2_stdev, fmt="o")
    tension2_plot.set_title("Post-Swage Tension Average by Day")
    tension2_plot.set_xlabel("Date, Past 60 Days")
    tension2_plot.set_ylabel("Tension (g)")
    tension2_plot.set_xticks(dates[::7])
    tension2_plot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    tension2_plot.grid()

    len_dif_plot.errorbar(dates, len_dif_avg, yerr=len_dif_stdev, fmt="o")
    len_dif_plot.set_title("Difference between Raw and Swage Length Average by Day")
    len_dif_plot.set_xlabel("Date, Past 60 Days")
    len_dif_plot.set_ylabel("Lenth Difference (mm)")
    len_dif_plot.set_xticks(dates[::7])
    len_dif_plot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    len_dif_plot.grid()

    tens_dif_plot.errorbar(dates, tens_dif_avg, yerr=tens_dif_stdev, fmt="o")
    tens_dif_plot.set_title("Difference between Pre and Post Swage Tension Average by Day")
    tens_dif_plot.set_xlabel("Date, Past 60 Days")
    tens_dif_plot.set_ylabel("Tension Difference (g)")
    tens_dif_plot.set_xticks(dates[::7])
    tens_dif_plot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    tens_dif_plot.grid()

    leak_plot.errorbar(dates, leak_avg, yerr=leak_stdev, fmt="o")
    leak_plot.set_title("Leak Rate Average by Day")
    leak_plot.set_xlabel("Date, Past 60 Days")
    leak_plot.set_ylabel("Leak Rate (mbar l/s)")
    leak_plot.set_xticks(dates[::7])
    leak_plot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    leak_plot.grid()

    dark_plot.errorbar(dates, dark_avg, yerr=dark_stdev, fmt="o")
    dark_plot.set_title("Dark Current Average by Day")
    dark_plot.set_xlabel("Date, Past 60 Days")
    dark_plot.set_ylabel("Leak Rate (nA)")
    dark_plot.set_xticks(dates[::7])
    dark_plot.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    dark_plot.grid()


    plt.show()