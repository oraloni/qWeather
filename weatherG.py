import tkinter as tk
import numpy, math, datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implements defualt matplotlib key binding
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from qWeather import Forcast
import pandas

class Graphs():
    def __init__(self, location, root):
        self.location = location
        self.forObj = Forcast(location)
        self.forcast_data = self.forObj.forcast_data()
        self.root = root 

    def get_forcast_datetime_data(self):
        self.dtlist = []
        self.data_list = self.forcast_data['list']
        for entry in range(len(self.forcast_data['list'])):
            dt_struct = datetime.datetime.fromisoformat(self.forcast_data['list'][entry]['dt_txt']) 
            self.dtlist.append(dt_struct)
        return self.dtlist

    def parse_times(self):
        self.dtlist = Graphs(self.location, self.root)
        self.dtlist = self.dtlist.get_forcast_datetime_data()
        hours_ts_list = []
        dates_ts_list = []
        self.combined = []
        for i in range(len(self.dtlist)):
            hour_parse_struct = datetime.datetime.strftime(self.dtlist[i], '%H:%M')
            date_parse_struct = datetime.datetime.strftime(self.dtlist[i], '%d/%m')
            hours_ts_list.append(hour_parse_struct)
            dates_ts_list.append(date_parse_struct)
            self.combined.append(f'{date_parse_struct}-{hour_parse_struct}')
        return self.combined

    def get_temp_for_time(self):
        # forcast_data = forObj.forcast_data()
        self.temp_list = []
        self.data_list = self.forcast_data['list']
        for i in range(len(self.forcast_data['list'])):
            temp_data = math.floor(self.forcast_data['list'][i]['main']['temp'])
            self.temp_list.append(temp_data)
        return self.temp_list

    def data_dict_get(self, date_lst, temp_lst):
        self.data_dict = {}
        for count, date in enumerate(date_lst):
            self.data_dict[date] = temp_lst[count]
        return self.data_dict

    def graph_data(self):
        self.data = Graphs(self.location, self.root)
        self.times = self.data.parse_times()
        self.temp = self.data.get_temp_for_time()
        self.data_dict = self.data.data_dict_get(self.times, self.temp)
        # keys = [data_dict.key]
        #print(data['time'])
        #self.timetuple = tuple(self.data['time'])
        return {'time':list(self.data_dict.keys()), 'temp': list(self.data_dict.values())}

    def forcast_graph(self, x_size=5, y_size=6, dpi=70):
        self.data = Graphs(self.location, self.root)
        self.data = self.data.graph_data()
        self.dataframe = pandas.DataFrame(self.data, columns=['time', 'temp'] )
        self.figure = plt.Figure(figsize=(x_size, y_size), dpi=dpi, tight_layout=True, edgecolor='lightgrey')
        plt.style.use('fivethirtyeight')
        ax1 = self.figure.add_subplot(111)
        bar = FigureCanvasTkAgg(self.figure, self.root)
        bar.draw()
        # toolbar = NavigationToolbar2Tk(bar, self.root, pack_toolbar=False)
        # toolbar.update()
        # toolbar.pack(side=tk.TOP, fill=tk.X)
        bar.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.dataframe = self.dataframe[['temp','time']]
        self.dataframe.plot(kind='line', legend=True, ax=ax1)
        ax1.set_title('Forecast')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Tempatures')

        ax1.set_xticks(range(len(self.data['time'])))
        ax1.set_xticklabels(self.data['time'], rotation=60)
        ax1.xaxis.set_major_locator(plt.MaxNLocator(15))

def main():
    root = tk.Tk() 
    root.wm_title('Embaddiding in TK')
    root.geometry('1000x1000')

    forcast = Graphs('Kfar Saba', root)
    forcast.forcast_graph()
    tk.mainloop()

if __name__ == "__main__":
    main()

