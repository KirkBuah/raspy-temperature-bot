import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines
import numpy as np
from sensor import TemperatureSensor
from datetime import datetime


class Graph:
    def __init__(self, n=24):
        # Fetch data from database, n=1 corresponds to 12 readings (1 hour)
        ts = TemperatureSensor()
        conn = ts.connect_to_db("./database.db")
        self.data = ts.read_from_db(n*12, conn)
        # Close connection
        conn.close()
        # Make tuples for each data type, dates are converted from epoch to datetime
        self.temperature = (d[0] for d in self.data)
        self.humidity = (d[1] for d in self.data)
        self.dates = (datetime.fromtimestamp(d[2]) for d in self.data)

        # Make a dew point tuple
        self.dewpoint = (self.dewpoint_from_data(d[0], d[1]) for d in self.data)

    @staticmethod
    def dewpoint_from_data(temperature, humidity):
        # This function returns the dewpoint from temperature and relative humidity
        a = 17.62
        b = 243.12

        gamma = np.log(humidity / 100) + ((a * temperature) / (b + temperature))
        return (b * gamma) / (a - gamma)

    def make_graph(self):

        # Make a graph containing temperature, humidity and dew point in the same figure

        # Define variables
        temperature = self.temperature
        humidity = self.humidity
        dewpoint = self.dewpoint
        dates = list(self.dates)
        # Prepare axes and set title
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax3 = ax1.twinx()
        fig.suptitle('Temperature and humidity plot of the last 24 hours')

        # Set datemin and datemax for the graph x axis limit
        datemin = dates[0]
        datemax = dates[-1]

        # Set Hour Locator
        hours = mdates.HourLocator()
        hours_fmt = mdates.DateFormatter('%H')

        # Plot temperature
        ax1.plot(dates, temperature, color='orangered')
        ax1.set_ylabel('Temperature (°C)', color='orangered')
        ax1.set_ylim(10, 30)
        ax1.set_yticks(np.arange(10, 30 + 1, 1))
        ax1.tick_params(axis='y', labelcolor='orangered')
        ax1.xaxis.set_major_locator(hours)
        ax1.xaxis.set_major_formatter(hours_fmt)
        ax1.grid(axis='y')
        ax1.grid(axis='x', linestyle='--', linewidth=0.5)
        ax1.set_xlim(datemax, datemin)

        # Plot humidity
        ax2.plot(dates, humidity, color='steelblue')
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

        # Plot dew point
        ax3.plot(dates, dewpoint, color='forestgreen')
        ax3.set_ylim(10, 30)
        ax3.set_yticks(np.arange(10, 30 + 1, 1))
        ax3.xaxis.set_major_locator(hours)
        ax3.xaxis.set_major_formatter(hours_fmt)
        ax3.set_xlim(datemax, datemin)
        ax3.set_axis_off()

        # Add legend
        templabel = mlines.Line2D([], [], color='orangered', label='Temperature')
        humiditylabel = mlines.Line2D([], [], color='steelblue', label='Humidity')
        dewlabel = mlines.Line2D([], [], color='forestgreen', label='Dew Point')

        plt.legend(handles=[templabel, humiditylabel, dewlabel])

        # Get current figure and save it
        fig = plt.gcf()
        fig.set_size_inches((10.3, 8), forward=False)
        fig.savefig('./tmp/temperature.png', dpi=500)
