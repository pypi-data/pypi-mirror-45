#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

import pandas as pd
import datetime
import matplotlib.dates as mdates

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU

def sleep_time_to_sleep_datetime(date, time):
    if time is not None:
        if time.hour < 12:
            date += datetime.timedelta(days=1)
        return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute)
    else:
        return None


def wake_up_time_to_wake_up_datetime(date, time):
    if time is not None:
        return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute)
    else:
        return None


class PlotCanvas(FigureCanvas):
    """This is a Matplotlib QWidget.

    See https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html
    """

    def __init__(self, data, parent, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

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
        #data = np.array(self.data._data)
        timemg_data = self.data

        if not init:
            self.axes.cla()

        try:
            #x = data[:, self.date_column_index]
            #dti = pd.DatetimeIndex(x)
            #s = pd.Series(np.ones(dti.shape), index=dti)

            #s.resample('1d').count().plot.bar(color="blue", alpha=0.5, ax=self.axes)

            DATE_LABEL = 'Date'
            WAKE_UP_LABEL = 'Wake up'
            SLEEP_LABEL = 'Sleep'

            date_index = timemg_data.headers.index(DATE_LABEL)
            wake_up_index = timemg_data.headers.index(WAKE_UP_LABEL)
            sleep_index = timemg_data.headers.index(SLEEP_LABEL)

            date_list =    [timemg_data.get_data(record_index, date_index)    for record_index in range(timemg_data.num_rows)]
            wake_up_list = [timemg_data.get_data(record_index, wake_up_index) for record_index in range(timemg_data.num_rows)]
            sleep_list   = [timemg_data.get_data(record_index, sleep_index)   for record_index in range(timemg_data.num_rows)]

            data_list = [
                            [
                                wake_up_time_to_wake_up_datetime(record_date, wake_up_time),
                                sleep_time_to_sleep_datetime(record_date, sleep_time)
                            ] for record_date, wake_up_time, sleep_time in zip(date_list, wake_up_list, sleep_list)
                        ]

            df = pd.DataFrame(data_list, columns=("wakeup", "bedtime"), index=pd.to_datetime(date_list))

            # BTSHIFT

            BED_TIME_REFERENCE = '22 h 30 m'

            df["btshift"] = df.bedtime - df.index

            df["btshift"] = df.btshift - pd.Timedelta(BED_TIME_REFERENCE)
            df["btshift"] = df.btshift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

            # WUSHIFT

            WAKE_UP_TIME_REFERENCE = '6 h 45 m'

            df["wushift"] = df.wakeup - df.index

            df["wushift"] = df.wushift - pd.Timedelta(WAKE_UP_TIME_REFERENCE)
            df["wushift"] = df.wushift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

            # Plot

            df[['btshift', 'wushift']].plot(x_compat=True, ax=self.axes)

            ###################################

            # set locator
            self.axes.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
            self.axes.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

            #ax.yaxis.set_major_locator(mdates.HourLocator())

            # set formatter
            self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
            #self.axes.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))

            # set font and rotation for date tick labels
            self.fig.autofmt_xdate()

            #s.plot(ax=self.axes)         # TODO
            #s.groupby(s.time).count().plot(ax=self.axes)         # TODO
            #self.axes.plot(x, y)
        except IndexError as e:
            # Happen when data is empty
            pass

        if not init:
            self.draw()
