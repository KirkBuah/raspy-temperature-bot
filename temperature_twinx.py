#!/bin/python3

import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines
import numpy as np
import datetime
from scipy.signal import find_peaks, peak_prominences


def load_obj(filepath):
    with open(filepath, 'r') as fp:
        data = json.load(fp)
    return data


def temp_graph(filepath, N, temp_lowerlimit=10, temp_upperlimit=30):  # N is the number of hours you want to be displayed
    def load_obj(filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return data

    tempdict = load_obj(filepath)

    temperature = []
    humidity = []
    dewpoint = []
    dewpointError = []
    dates = list(tempdict.keys())
    yerrHum = 2
    yerrTemp = 0.5

    for i in range(-N * 12, 0):
        temperature.append(list(tempdict.values())[i][0])
        humidity.append(list(tempdict.values())[i][1])
        try:
            dewpoint.append(list(tempdict.values())[i][2][0])
            dewpointError.append(list(tempdict.values())[i][2][1])
        except:
            dewpoint.append(None)
            dewpointError.append(None)

    x_values = [datetime.datetime.strptime(d, "%Y/%m/%d - %H:%M:%S") for d in dates][-N * 12:]  # 12 readings every hour
    datemin = x_values[-1]
    datemax = x_values[-12 * N]

    # make graphs
    if N <= 24:
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()
        fig.suptitle('Temperature and humidity plot of the last {} hours'.format(N))

        hours = mdates.HourLocator()
        hours_fmt = mdates.DateFormatter('%H')

        ax1.plot(x_values, temperature, color='orangered')
        ax1.set_ylabel('Temperature (°C)', color='orangered')
        ax1.set_ylim(temp_lowerlimit, temp_upperlimit)
        ax1.set_yticks(np.arange(temp_lowerlimit, temp_upperlimit + 1, (temp_upperlimit - temp_lowerlimit) / 20))
        ax1.tick_params(axis='y', labelcolor='orangered')
        ax1.xaxis.set_major_locator(hours)
        ax1.xaxis.set_major_formatter(hours_fmt)
        ax1.grid(axis='y')
        ax1.grid(axis='x', linestyle='--', linewidth=0.5)
        ax1.set_xlim(datemax, datemin)
        h1, l1 = ax1.get_legend_handles_labels()

        ax2.plot(x_values, humidity, color='steelblue')
        ax2.set_xlabel('time (h)')
        ax2.set_ylabel('Relative Humidity (%)', color='steelblue')
        ax2.set_ylim(0, 100)
        ax2.set_yticks(np.arange(0, 100 + 1, 5))
        ax2.tick_params(axis='y', labelcolor='steelblue')
        ax2.xaxis.set_major_locator(hours)
        ax2.xaxis.set_major_formatter(hours_fmt)
        ax2.grid(axis='y')
        ax2.grid(axis='x', linestyle='--', linewidth=0.5)
        ax2.set_xlim(datemax, datemin)
        h2, l2 = ax2.get_legend_handles_labels()

        ax3.plot(x_values, dewpoint, color='limegreen')
        ax3.set_ylim(temp_lowerlimit, temp_upperlimit)
        ax3.set_yticks(np.arange(temp_lowerlimit, temp_upperlimit + 1, (temp_upperlimit - temp_lowerlimit) / 20))
        ax3.xaxis.set_major_locator(hours)
        ax3.xaxis.set_major_formatter(hours_fmt)
        ax3.set_xlim(datemax, datemin)
        ax3.set_axis_off()
        h3, l3 = ax3.get_legend_handles_labels()

        # add legend
        tempLabel = mlines.Line2D([], [], color='orangered', label='Temperature')
        humidityLabel = mlines.Line2D([], [], color='steelblue', label='Humidity')
        dewLabel = mlines.Line2D([], [], color='limegreen', label='Dew Point')

        plt.legend(handles=[tempLabel, humidityLabel, dewLabel])

        fig = plt.gcf()
        fig.set_size_inches((10.3, 8), forward=False)
        fig.savefig('./tmp/temperature.png', dpi=500)
        plt.show()

    else:
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()
        fig.suptitle('Temperature and humidity plot of the last {} hours'.format(N))

        locator = mdates.WeekdayLocator()
        locator_fmt = mdates.DateFormatter('%d/%m')
        linewidth = 1

        ax1.plot(x_values, temperature, color='orangered', linewidth=linewidth)
        ax1.set_ylabel('Temperature (°C)', color='orangered')
        ax1.set_ylim(temp_lowerlimit, temp_upperlimit)
        ax1.set_yticks(np.arange(temp_lowerlimit, temp_upperlimit + 1, (temp_upperlimit - temp_lowerlimit) / 20))
        ax1.tick_params(axis='y', labelcolor='orangered')
        ax1.xaxis.set_major_locator(locator)
        ax1.xaxis.set_major_formatter(locator_fmt)
        ax1.grid(axis='y')
        ax1.grid(axis='x', linestyle='--', linewidth=0.5)
        ax1.set_xlim(datemax, datemin)
        h1, l1 = ax1.get_legend_handles_labels()
        '''find temperature peaks which correspond to the radiator turning on'''

        peaks, _ = find_peaks(temperature, prominence=(None, 0.6))
        prominences = peak_prominences(temperature, peaks)[0]

        ax2.plot(x_values, humidity, color='steelblue', linewidth=linewidth)
        ax2.set_xlabel('time (h)')
        ax2.set_ylabel('Relative Humidity (%)', color='steelblue')
        ax2.set_ylim(0, 100)
        ax2.set_yticks(np.arange(0, 100 + 1, 5))
        ax2.tick_params(axis='y', labelcolor='steelblue')
        ax2.xaxis.set_major_locator(locator)
        ax2.xaxis.set_major_formatter(locator_fmt)
        ax2.grid(axis='y')
        ax2.grid(axis='x', linestyle='--', linewidth=0.5)
        ax2.set_xlim(datemax, datemin)
        h2, l2 = ax2.get_legend_handles_labels()

        ax3.plot(x_values, dewpoint, color='limegreen', linewidth=linewidth)
        ax3.set_ylim(temp_lowerlimit, temp_upperlimit)
        ax3.set_yticks(np.arange(temp_lowerlimit, temp_upperlimit + 1, (temp_upperlimit - temp_lowerlimit) / 20))
        ax3.xaxis.set_major_locator(locator)
        ax3.xaxis.set_major_formatter(locator_fmt)
        ax3.set_xlim(datemax, datemin)
        ax3.set_axis_off()
        h3, l3 = ax3.get_legend_handles_labels()

        # add legend
        tempLabel = mlines.Line2D([], [], color='orangered', label='Temperature')
        humidityLabel = mlines.Line2D([], [], color='steelblue', label='Humidity')
        dewLabel = mlines.Line2D([], [], color='limegreen', label='Dew Point')

        plt.legend(handles=[tempLabel, humidityLabel, dewLabel])

        fig = plt.gcf()
        fig.set_size_inches((10.3, 8), forward=False)
        fig.savefig('./tmp/temperature.png', dpi=500)
        plt.show()


if __name__ == '__main__':
    a = temp_graph('./obj/temperature.json', 24 * 30, 0, 30)
