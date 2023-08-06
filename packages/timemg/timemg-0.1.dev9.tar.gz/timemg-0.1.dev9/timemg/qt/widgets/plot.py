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

def datetime_builder(date, time, day_init_hour=0):
    if time is not None:
        if time.hour < day_init_hour:
            date += datetime.timedelta(days=1)
        return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute)
    else:
        return None

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
        #data = np.array(self.data._data)
        timemg_data = self.data

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

            DATE_LABEL = 'Date'
            WAKE_UP_LABEL = 'Wake up'
            SLEEP_LABEL = 'Sleep'
            WORK_IN_LABEL = 'W. in'
            WORK_OUT_LABEL = 'W. out'

            date_index = timemg_data.headers.index(DATE_LABEL)
            wake_up_index = timemg_data.headers.index(WAKE_UP_LABEL)
            sleep_index   = timemg_data.headers.index(SLEEP_LABEL)
            work_in_index  = timemg_data.headers.index(WORK_IN_LABEL)
            work_out_index = timemg_data.headers.index(WORK_OUT_LABEL)

            date_list     = [timemg_data.get_data(record_index, date_index)     for record_index in range(timemg_data.num_rows)]
            wake_up_list  = [timemg_data.get_data(record_index, wake_up_index)  for record_index in range(timemg_data.num_rows)]
            sleep_list    = [timemg_data.get_data(record_index, sleep_index)    for record_index in range(timemg_data.num_rows)]
            work_in_list  = [timemg_data.get_data(record_index, work_in_index)  for record_index in range(timemg_data.num_rows)]
            work_out_list = [timemg_data.get_data(record_index, work_out_index) for record_index in range(timemg_data.num_rows)]

            data_list = [
                            [
                                datetime_builder(record_date, wake_up_time),
                                datetime_builder(record_date, sleep_time, day_init_hour=12),
                                datetime_builder(record_date, work_in_time),
                                datetime_builder(record_date, work_out_time)
                            ] for record_date, wake_up_time, sleep_time, work_in_time, work_out_time in zip(date_list, wake_up_list, sleep_list, work_in_list, work_out_list)
                        ]

            df = pd.DataFrame(data_list, columns=("wakeup", "bedtime", "work_in", "work_out"), index=pd.to_datetime(date_list))

            # WUSHIFT

            WAKE_UP_TIME_REFERENCE = '6 h 45 m 59 s'

            df["wushift"] = df.wakeup - df.index

            df["wushift"] = df.wushift - pd.Timedelta(WAKE_UP_TIME_REFERENCE)
            df["wushift"] = df.wushift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

            # BTSHIFT

            BED_TIME_REFERENCE = '22 h 30 m 59 s'

            df["btshift"] = df.bedtime - df.index

            df["btshift"] = df.btshift - pd.Timedelta(BED_TIME_REFERENCE)
            df["btshift"] = df.btshift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

            # WISHIFT

            WORK_IN_TIME_REFERENCE = '9 h 15 m 59 s'

            df["wishift"] = df.work_in - df.index

            df["wishift"] = df.wishift - pd.Timedelta(WORK_IN_TIME_REFERENCE)
            df["wishift"] = df.wishift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

            # WOSHIFT

            WORK_OUT_TIME_REFERENCE = '18 h 30 m 59 s'

            df["woshift"] = df.work_out - df.index

            df["woshift"] = df.woshift - pd.Timedelta(WORK_OUT_TIME_REFERENCE)
            df["woshift"] = df.woshift.apply(lambda x: x.total_seconds() / 60.)  # Convert to float

            ###################################

            df = df.sort_index()
            df['date'] = df.index

            df['date_fmt'] = df['date'].dt.strftime('%a %d/%m')
            df.loc[::2, 'date_fmt'] = ''

            # Plot 1 ###################################

            tk1 = list(reversed(-np.arange(0, -df.wushift.min(), 30)))
            tk2 = list(np.arange(0, df.wushift.max(), 30))

            df.plot(x='date_fmt', y='wushift', kind='bar', yticks=tk1 + tk2, ax=self.ax1)
            
            # set locator
            #self.ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
            ##self.ax2.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

            # set formatter
            ##self.ax2.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
            #self.ax2.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))

            # set font and rotation for date tick labels
            #self.fig.autofmt_xdate()

            self.ax1.grid(True, axis="y", linestyle=':', alpha=0.75)

            self.ax1.set_title("Wake up shift")
            self.ax1.set_xlabel("")
            self.ax1.set_ylabel("Minutes")

            if self.ax1.get_legend() is not None:
                self.ax1.get_legend().remove()

            # Plot 2 ###################################

            tk1 = list(reversed(-np.arange(0, -df.btshift.min(), 30)))
            tk2 = list(np.arange(0, df.btshift.max(), 30))

            df.plot(x='date_fmt', y='btshift', kind='bar', yticks=tk1 + tk2, ax=self.ax2)
            
            # set locator
            #self.ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=MO))
            #self.ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))

            # set formatter
            ##self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%a %d-%m'))
            #self.ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))

            # set font and rotation for date tick labels
            #self.fig.autofmt_xdate()

            self.ax2.grid(True, axis="y", linestyle=':', alpha=0.75)

            self.ax2.set_title("Bed time shift")
            self.ax2.set_xlabel("")
            self.ax2.set_ylabel("Minutes")

            if self.ax2.get_legend() is not None:
                self.ax2.get_legend().remove()

            # Plot 3 ###################################

            tk1 = list(reversed(-np.arange(0, -df.wishift.min(), 30)))
            tk2 = list(np.arange(0, df.wishift.max(), 30))

            df.plot(x='date_fmt', y='wishift', kind='bar', yticks=tk1 + tk2, ax=self.ax3)

            self.ax3.grid(True, axis="y", linestyle=':', alpha=0.75)

            self.ax3.set_title("Work in shift")
            self.ax3.set_xlabel("")
            self.ax3.set_ylabel("Minutes")

            if self.ax3.get_legend() is not None:
                self.ax3.get_legend().remove()

            # Plot 4 ###################################

            tk1 = list(reversed(-np.arange(0, -df.woshift.min(), 30)))
            tk2 = list(np.arange(0, df.woshift.max(), 30))

            df.plot(x='date_fmt', y='woshift', kind='bar', yticks=tk1 + tk2, ax=self.ax4)

            self.ax4.grid(True, axis="y", linestyle=':', alpha=0.75)

            self.ax4.set_title("Work out shift")
            self.ax4.set_xlabel("")
            self.ax4.set_ylabel("Minutes")

            if self.ax4.get_legend() is not None:
                self.ax4.get_legend().remove()

            # Plot 5 ###################################

            self.ax5.set_title("Work duration")
            self.ax5.set_xlabel("")
            self.ax5.set_ylabel("Hours")

            if self.ax5.get_legend() is not None:
                self.ax5.get_legend().remove()

            # Plot 6 ###################################

            self.ax6.set_title("Sleep duration")
            self.ax6.set_xlabel("")
            self.ax6.set_ylabel("Hours")

            if self.ax6.get_legend() is not None:
                self.ax6.get_legend().remove()

            ###################################

            self.fig.tight_layout()
            
        except IndexError as e:
            # Happen when data is empty
            print(e)
            #pass

        if not init:
            self.draw()
