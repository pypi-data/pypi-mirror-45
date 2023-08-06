#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import pandas as pd
import datetime
import matplotlib.dates as mdates

import math

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#import seaborn as sns

from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU

BLUE = '#1f77b4'
RED = '#d62728'
YELLOW = '#ff7f0e'
GREEN = '#2ca02c'

def make_datetime(date, time, day_init_hour=0):
    if time is not None:
        if time.hour < day_init_hour:
            date += datetime.timedelta(days=1)
        return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute)
    else:
        return None


def make_dataframe(timemg_data):
    DATE_LABEL = 'Date'
    WAKE_UP_LABEL = 'Wake up'
    SLEEP_LABEL = 'Sleep'
    WORK_IN_LABEL = 'W. in'
    WORK_OUT_LABEL = 'W. out'

    date_index     = timemg_data.headers.index(DATE_LABEL)
    wake_up_index  = timemg_data.headers.index(WAKE_UP_LABEL)
    sleep_index    = timemg_data.headers.index(SLEEP_LABEL)
    work_in_index  = timemg_data.headers.index(WORK_IN_LABEL)
    work_out_index = timemg_data.headers.index(WORK_OUT_LABEL)

    date_list     = [timemg_data.get_data(record_index, date_index)     for record_index in range(timemg_data.num_rows)]
    wake_up_list  = [timemg_data.get_data(record_index, wake_up_index)  for record_index in range(timemg_data.num_rows)]
    sleep_list    = [timemg_data.get_data(record_index, sleep_index)    for record_index in range(timemg_data.num_rows)]
    work_in_list  = [timemg_data.get_data(record_index, work_in_index)  for record_index in range(timemg_data.num_rows)]
    work_out_list = [timemg_data.get_data(record_index, work_out_index) for record_index in range(timemg_data.num_rows)]

    data_list = [
                    [
                        make_datetime(record_date, wake_up_time),
                        make_datetime(record_date, sleep_time, day_init_hour=12),
                        make_datetime(record_date, work_in_time),
                        make_datetime(record_date, work_out_time)
                    ] for record_date, wake_up_time, sleep_time, work_in_time, work_out_time in zip(date_list, wake_up_list, sleep_list, work_in_list, work_out_list)
                ]

    df = pd.DataFrame(data_list, columns=("wakeup", "bedtime", "work_in", "work_out"), index=pd.to_datetime(date_list))

    # WUSHIFT #########################

    WAKE_UP_TIME_REFERENCE = '6 h 45 m 59 s'

    df["wushift"] = df.wakeup - df.index

    df["wushift"] = df.wushift - pd.Timedelta(WAKE_UP_TIME_REFERENCE)
    df["wushift"] = df.wushift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

    # BTSHIFT #########################

    BED_TIME_REFERENCE = '22 h 30 m 59 s'

    df["btshift"] = df.bedtime - df.index

    df["btshift"] = df.btshift - pd.Timedelta(BED_TIME_REFERENCE)
    df["btshift"] = df.btshift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

    # WISHIFT #########################

    WORK_IN_TIME_REFERENCE = '9 h 15 m 59 s'

    df["wishift"] = df.work_in - df.index

    df["wishift"] = df.wishift - pd.Timedelta(WORK_IN_TIME_REFERENCE)
    df["wishift"] = df.wishift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

    # WOSHIFT #########################

    WORK_OUT_TIME_REFERENCE = '18 h 30 m 59 s'

    df["woshift"] = df.work_out - df.index

    df["woshift"] = df.woshift - pd.Timedelta(WORK_OUT_TIME_REFERENCE)
    df["woshift"] = df.woshift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

    # WORK DURATION ###################

    df['work_duration'] = df.work_out - df.work_in

    df['work_duration_hrs'] = df.work_duration / np.timedelta64(1, 'h')

    # SLEEP DURATION ##################

    df['date'] = df.index

    # Detect whether 2 rows are not 2 consecutive days
    df['compute_sleep_duration'] = (df.date.diff() == pd.Timedelta('1 days'))

    # Compute sleep duration
    df['sleep_duration'] = df['wakeup'] - df['bedtime'].shift()

    # Put sleep duration to "NaT" when the previous row is not the previous day
    df.loc[~df.compute_sleep_duration, 'sleep_duration'] = pd.NaT

    df['sleep_duration_hrs'] = df.sleep_duration / np.timedelta64(1, 'h')

    # Categories

    df['sleep_duration_class'] = 'bad'
    df.loc[(df.sleep_duration_hrs >= 8) & (df.sleep_duration_hrs <=  9), 'sleep_duration_class'] = 'good'
    df.loc[(df.sleep_duration_hrs >= 7) & (df.sleep_duration_hrs <   8), 'sleep_duration_class'] = 'medium'
    df.loc[(df.sleep_duration_hrs  > 9) & (df.sleep_duration_hrs <= 10), 'sleep_duration_class'] = 'medium'

    ###################################

    df = df.sort_index()

    return df


def plot_wake_up_shift(df, ax):
    tk1 = list(reversed(-np.arange(0, -df.wushift.min(), 30)))
    tk2 = list(np.arange(0, df.wushift.max(), 30))

    df.plot(x='date_fmt', y='wushift', kind='bar', color=BLUE, yticks=tk1 + tk2, ax=ax)
    
    # set locator
    #self.ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
    ##self.ax2.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

    # set formatter
    ##self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
    #self.ax2.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))

    # set font and rotation for date tick labels
    #self.fig.autofmt_xdate()

    ax.grid(True, axis="y", linestyle=':', alpha=0.75)

    ax.set_title("Wake up shift")
    ax.set_xlabel("")
    ax.set_ylabel("Minutes")

    if ax.get_legend() is not None:
        ax.get_legend().remove()


def plot_bed_time_shift(df, ax):
    tk1 = list(reversed(-np.arange(0, -df.btshift.min(), 30)))
    tk2 = list(np.arange(0, df.btshift.max(), 30))

    df.plot(x='date_fmt', y='btshift', kind='bar', color=BLUE, yticks=tk1 + tk2, ax=ax)
    
    # set locator
    #self.ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
    #self.ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

    # set formatter
    ##self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
    #self.ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))

    # set font and rotation for date tick labels
    #self.fig.autofmt_xdate()

    ax.grid(True, axis="y", linestyle=':', alpha=0.75)

    ax.set_title("Bed time shift")
    ax.set_xlabel("")
    ax.set_ylabel("Minutes")

    if ax.get_legend() is not None:
        ax.get_legend().remove()


def plot_work_in_shift(df, ax):
    tk1 = list(reversed(-np.arange(0, -df.wishift.min(), 30)))
    tk2 = list(np.arange(0, df.wishift.max(), 30))

    df.plot(x='date_fmt', y='wishift', kind='bar', color=BLUE, yticks=tk1 + tk2, ax=ax)

    ax.grid(True, axis="y", linestyle=':', alpha=0.75)

    ax.set_title("Work in shift")
    ax.set_xlabel("")
    ax.set_ylabel("Minutes")

    if ax.get_legend() is not None:
        ax.get_legend().remove()


def plot_work_out_shift(df, ax):
    tk1 = list(reversed(-np.arange(0, -df.woshift.min(), 30)))
    tk2 = list(np.arange(0, df.woshift.max(), 30))

    df.plot(x='date_fmt', y='woshift', kind='bar', color=BLUE, yticks=tk1 + tk2, ax=ax)

    ax.grid(True, axis="y", linestyle=':', alpha=0.75)

    ax.set_title("Work out shift")
    ax.set_xlabel("")
    ax.set_ylabel("Minutes")

    if ax.get_legend() is not None:
        ax.get_legend().remove()


def plot_work_duration(df, ax):
    NORMAL_WEEKLY_WORK_HOURS = 39

    tk = list(np.arange(0,      # math.floor(df.work_duration_hrs.min()),
                        math.ceil(df.work_duration_hrs.max()) + 1,
                        1))

    df.plot(x='date_fmt', y='work_duration_hrs', kind='bar', color=BLUE, yticks=tk, ax=ax)

    ax.grid(True, axis="y", linestyle=':', alpha=0.75)

    ax.axhline(NORMAL_WEEKLY_WORK_HOURS / 5., color='red', linestyle=':')

    ax.set_title("Work duration")
    ax.set_xlabel("")
    ax.set_ylabel("Hours")

    if ax.get_legend() is not None:
        ax.get_legend().remove()


def plot_sleep_duration(df, ax):
    NORMAL_SLEEP_HOURS = 8

    tk = list(np.arange(0,      # math.floor(df.sleep_duration_hrs.min()),
                        math.ceil(df.sleep_duration_hrs.max()) + 1,
                        1))

    df.plot(x='date_fmt', y='sleep_duration_hrs', kind='bar', color=BLUE, yticks=tk, ax=ax)
    #sns.barplot(x="date", y="sleep_duration_hrs", data=df, hue="sleep_duration_class", ax=ax)

    ax.grid(True, axis="y", linestyle=':', alpha=0.75)

    ax.axhline(NORMAL_SLEEP_HOURS + 1, color='red', linestyle=':')
    ax.axhline(NORMAL_SLEEP_HOURS, color='red', linestyle='--')
    ax.axhline(NORMAL_SLEEP_HOURS - 1, color='red', linestyle=':')

    ax.set_title("Sleep duration")
    ax.set_xlabel("")
    ax.set_ylabel("Hours")

    if ax.get_legend() is not None:
        ax.get_legend().remove()


class PlotCanvas(FigureCanvas):
    """This is a Matplotlib QWidget.

    See https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """

    def __init__(self, data, parent, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        nrows = 3
        ncols = 2
        self.ax1 = self.fig.add_subplot(nrows, ncols, 1)
        self.ax2 = self.fig.add_subplot(nrows, ncols, 2)
        self.ax3 = self.fig.add_subplot(nrows, ncols, 3)
        self.ax4 = self.fig.add_subplot(nrows, ncols, 4)
        self.ax5 = self.fig.add_subplot(nrows, ncols, 5)
        self.ax6 = self.fig.add_subplot(nrows, ncols, 6)

        self.data = data
        self.date_column_index = data.headers.index("Date")

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def compute_initial_figure(self):
        self.update_figure(init=True)


    def update_figure(self, init=False):

        if not init:
            self.ax1.cla()
            self.ax2.cla()
            self.ax3.cla()
            self.ax4.cla()
            self.ax5.cla()
            self.ax6.cla()

        try:
            #x = data[:, self.date_column_index]
            #dti = pd.DatetimeIndex(x)
            #s = pd.Series(np.ones(dti.shape), index=dti)

            #s.resample('1d').count().plot.bar(color="blue", alpha=0.5, ax=self.axes)

            df = make_dataframe(self.data)

            df['date'] = df.index

            df['date_fmt'] = df['date'].dt.strftime('%a %d/%m')
            df.loc[::2, 'date_fmt'] = ''

            ###################################

            plot_wake_up_shift(df, self.ax2)

            plot_bed_time_shift(df, self.ax4)

            plot_work_in_shift(df, self.ax1)

            plot_work_out_shift(df, self.ax3)

            plot_work_duration(df, self.ax5)

            plot_sleep_duration(df, self.ax6)

            ###################################

            self.fig.tight_layout()
            
        except IndexError as e:
            # Happen when data is empty
            print(e)
            #pass

        if not init:
            self.draw()
