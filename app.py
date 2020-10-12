import tkinter as tk
from tkinter import ttk
from qWeather import Weather, Forcast
import time
from weatherG import Graphs


class Root(tk.Tk):
    # Top Level window
    def __init__(self):
        super().__init__()
        self.app_name = 'qWeather v.2.5'
        self.title('qWeather v.2.5')
        self.geometry('820x640')
        # Defualt location
        self.location = 'Kfar Saba'
        self.configure()

        self.tab_control = ttk.Notebook(self, padding=5)
        self.tab_control.grid(row=0, column=0)
        # tab1 - General information
        self.tab1 = ttk.Frame(self.tab_control, width = 600, height = 600, relief = tk.SUNKEN)
        #ttk.Style().configure("TFrame", background='lightgrey')
        # tab2 - Weather maps
        self.tab_control.add(self.tab1, text = 'Local Weather')
        self.tab2 = ttk.Frame(self.tab_control, width = 800, height = 700, relief = tk.SUNKEN)
        self.tab_control.add(self.tab2, text = 'Forecast')
        self.weather = Weather()
        self.name_font = ('Qualy', '26', 'bold', 'bold')
        self.description_font = ('Times', '18', 'bold')
        self.location_font = ('Times', '16', 'underline')
        self.data_font = ('Times', '16', 'bold')
        self.button_font = ('Times', '13', 'bold')
        
    def widgets(self):
        self.data = self.weather.today_weather_data(self.location)
        # Font obj.

        # Name Frame and Label
        self.name_frame = tk.Frame(self.tab1)
        self.name_label = tk.Label(self.name_frame, text=self.app_name, font=self.name_font)
        self.name_frame.grid(row=0, column=0, columnspan=4, padx=50, pady=20, ipadx=10, ipady=5, sticky='nwse')
        self.name_label.pack(side=tk.LEFT)
        # Location
        self.location_frame = tk.Frame(self.tab1)
        self.location_label = tk.Label(self.location_frame, text=self.location.title(), font=self.location_font, padx=60)
        self.location_frame.grid(row=1, column=1, padx=80, sticky='e')
        self.location_label.pack(side=tk.LEFT, fill=tk.X)
    # Data frame
        # General weather description

        self.description_text =  self.data['description']
        self.description_frame = tk.Frame(self.tab1)
        self.description_frame.grid(row=2, column=1, padx=128, pady=10, sticky='e')
        self.description_label = tk.Label(self.description_frame, text = self.description_text,
                                          font = self.description_font, anchor=tk.CENTER)
        self.description_label.grid(row=0, column=0, sticky='w')

        self.icon_img = self.weather.get_icon()

        self.icon_frame = tk.Frame(self.tab1)
        self.icon_frame.grid(row=1, column=3, padx=30, sticky='nesw')
        self.icon_label = tk.Label(self.icon_frame, image=self.icon_img, bg='grey88')
        self.icon_label.pack(side=tk.RIGHT)
        # detailed weather
        self.data_canvas = tk.Canvas(self.tab1)
        self.data_canvas.grid(row=3, column=1, rowspan=3, columnspan=2, pady=8, sticky='nwse')
        self.degLabel = tk.Label(self.data_canvas,
                                 text='Tempartures: ' + str(self.data['tempatures']) + ' cel',
                                 font=self.data_font, padx=20, pady=20)
        self.degLabel.grid(row=0, column=1)
        self.fills_like_label = tk.Label(self.data_canvas,
                                         text='Feels Like: ' + str(self.data['feels_like']) + ' cel',
                                         font=self.data_font, padx=20, pady=20)
        self.fills_like_label.grid(row=0, column=2)
        self.humidety_label = tk.Label(self.data_canvas,
                                 text='Humidty: ' + str(self.data['humidity']) + '%',
                                 font=self.data_font, padx=20, pady=20)
        self.humidety_label.grid(row=1, column=1, sticky='w')
        self.wind_speed_label = tk.Label(self.data_canvas,
                                         text='Wind Speed: ' + str(self.data['windspeed']) + ' kmh',
                                         font=self.data_font, padx=20, pady=20)
        self.wind_speed_label.grid(row=1, column=2)
        self.wind_direction_label = tk.Label(self.data_canvas,
                                         text='Wind Direction: ' + str(self.data['wind_direction']) + ' deg.',
                                         font=self.data_font, padx=20, pady=20)
        self.wind_direction_label.grid(row=2, column=2, sticky='e')
        self.clouds = tk.Label(self.data_canvas,
                                         text='Clouds: ' + str(self.data['clouds']) + '%',
                                         font=self.data_font, padx=20, pady=20)
        self.clouds.grid(row=2, column=1, sticky='w')

    # Buttons
        # Refresh button
        self.refresh_button= tk.Button(self.tab1, text = 'Update Data',
                                 font=self.button_font, command=self.refresh_data,
                                 bg='lightgrey', padx=33, pady=0, height=2, width=10)
        self.refresh_button.grid(row=7, column=3)
        self.refresh_button.bind()
        # Change location
        change_location_button= tk.Button(self.tab1, text ='Change Location',
                                font=self.button_font, command=self.change_location, padx=19, pady=0, height=2)
        change_location_button.grid(row=8, column=3)
    # Auto refresh labelframe choise
        auto_font = ('Times', '13', 'bold')
        frame_text_font  = ('Times', '10')
        # self.auto_refresh_label = tk.Label(self, text='auto update and refresh', font=auto_font)
        # self.auto_refresh_label.grid(row=8, column=0, sticky='e')
        self.auto_label = tk.LabelFrame(self.tab1, text='Auto Update', font=frame_text_font, bg='lightgrey', bd=3)
        self.auto_label.grid(row=8, column=0, sticky='sw', padx = 20, pady=0)
        self.check_status = tk.IntVar()
        self.enable_auto_refresh = tk.Radiobutton(self.auto_label, text= 'Enable', font=auto_font, value=1,
                                                 variable=self.check_status, command=self.auto_refresh_status)
        self.enable_auto_refresh.grid(row=7, column=0)
        self.disable_auto_refresh = tk.Radiobutton(self.auto_label, text= 'Disable', font=auto_font, value=2,
                                                 variable=self.check_status, command=self.auto_refresh_status)
        self.disable_auto_refresh.grid(row=8, column=0)

        # Last data update stamp label
        last_update_font = ('Times', '8', 'bold')
        last_update = self.weather.update_time()
        self.update_label = tk.Label(self.tab1, text='Last Data Update:\n' + last_update, font=last_update_font)
        self.update_label.grid(row=8, column=1, sticky='sw')

    # Enable/Disable auto refresh
    def auto_refresh_status(self):
        self.status = self.check_status.get()
        print(self.status)
        if self.status == 1:
            self.status = True
        else:
            self.status = False
        self.auto_refresh()

    # If auto refresh is enabled - data would refresh every 10 minutes
    def auto_refresh(self):
        print(self.status)
        if self.status:
            root.after(600000, self.refresh_data)
            root.after(600001, self.auto_refresh)

    def refresh_data(self):
        new_info = self.weather.today_weather_data(self.location)
        print (new_info)
        self.data.update(new_info)
        self.widgets()


    def change_location(self):
        # Create new window to enter new location
        self.location_window = tk.Toplevel(self)
        self.location_window.title('Change Location')
        self.location_window.geometry('390x150')
        # Fonts
        title_font = ('Times', '16', 'bold')
        help_font = ('Times', '9', 'bold')
        input_font = ('Times', '12')
        # Title label
        title_label = tk.Label(self.location_window, text="Set Location:", font=title_font)
        title_label.grid(row=0, column=0, columnspan=3, padx=25, pady=5)
        self.new_location = tk.StringVar()
        self.location_entry = tk.Entry(self.location_window, textvariable=self.new_location, font=input_font)
        self.location_entry.grid(row=2, column=0, columnspan=2, sticky='WE', padx=20)
        self.location_entry.focus_set()
        help_label = tk.Label(self.location_window, text='Foramt:  >Country\n \t    >City Name\n\
               \t   \t    >City Name, Country', anchor='n', font=help_font)
        help_label.grid(row=3, column=0 , padx=40, pady=0)
        submit_button = tk.Button(self.location_window, text='Submit', font=('Times', '13', 'bold'),
                                   command=self.update_location)
        submit_button.grid(row=2, column=2, padx=0, sticky='w')

    def update_location(self):
        try:
            entry_text = self.new_location.get()
            self.location = entry_text
            self.description_label.destroy()
            self.widgets()
            self.location_window.destroy()
            self.update_graph()
            self.forcast_update()
        except:
            unableLabel = tk.Label(self.location_window, text='Unable to find %s' % self.location)
            unableLabel.grid(row=1, column=0, sticky='w', padx=40)

    def forcast_graph(self):
        self.g_canvas = tk.Canvas(self.tab2)
        self.g_canvas.pack(side=tk.BOTTOM, fill=tk.X, ipady=100)
        self.graph = Graphs(self.location, self.g_canvas)
        self.weather_graph = self.graph.forcast_graph(1, 1, 60)
        
    def update_graph(self):
        self.g_canvas.destroy()
        self.forcast_graph()

    def forecast(self):
        self.forcast = Forcast(self.location)
        self.daily_forcast = self.forcast.daily_forcast()
        self.tomorrow_day_name = self.daily_forcast[0]['date'].strftime('%A')
        self.after_tomorrow_day_name = self.daily_forcast[1]['date'].strftime('%A')
        self.in_twodays_name = self.daily_forcast[2]['date'].strftime('%A')
        #print(tomorrow_day_name, after_tomorrow_day_name, in_twodays_name)
        day_name_label_font = ('Times', '18')
        self.f_canvas = tk.Canvas(self.tab2)
        self.f_canvas.pack(side=tk.TOP, fill=tk.BOTH)
        self.tomorrow_lb = tk.LabelFrame(self.f_canvas, text=self.tomorrow_day_name, font=day_name_label_font, borderwidth=5)
        self.tomorrow_lb.grid(row=0, column=0, padx=20, pady=10)
        #ttk.Style().configure("TLabelframe", background='black')
        self.after_tomorrow_lb = tk.LabelFrame(self.f_canvas, text=self.after_tomorrow_day_name, font=day_name_label_font, borderwidth=5)
        self.after_tomorrow_lb.grid(row=0, column=1, padx=20, pady=10)
        self.two_days_lb = tk.LabelFrame(self.f_canvas, text=self.in_twodays_name, font=day_name_label_font, borderwidth=5)
        self.two_days_lb.grid(row=0, column=2, padx=20, pady=10)
        # Tommorow
        self.tom_icon_img = self.forcast.forcast_icon(self.daily_forcast[0]['icon'])
        self.tom_icon_label = tk.Label(self.tomorrow_lb, image=self.tom_icon_img, bg='grey88', anchor='n')
        self.tom_icon_label.grid(row=1, column=0, sticky='n')
        self.tom_temp_frame = tk.Frame(self.tomorrow_lb)
        self.tom_temp_frame.grid(row=2, column=0)
        self.tom_def_label = tk.Label(self.tomorrow_lb, text=(self.daily_forcast[0]['description']), font=self.data_font, anchor='c')
        self.tom_def_label.grid(row=0, column=0)
        self.tom_min_temp_label = tk.Label(self.tom_temp_frame, text=('Min: %s cel.' % (self.daily_forcast[0]['min'])), font=self.data_font)
        self.tom_min_temp_label.grid(row=0, column=0, padx=40)
        self.tom_max_temp_label = tk.Label(self.tom_temp_frame, text=('Max: %s cel.' % (self.daily_forcast[0]['max'])), font=self.data_font)
        self.tom_max_temp_label.grid(row=1, column=0)
        # Day After Tommorow
        self.aft_icon_img = self.forcast.forcast_icon(self.daily_forcast[1]['icon'])
        self.aft_icon_label = tk.Label(self.after_tomorrow_lb, image=self.tom_icon_img, bg='grey88', anchor='n')
        self.aft_icon_label.grid(row=1, column=0, sticky='n')
        self.aft_temp_frame = tk.Frame(self.after_tomorrow_lb)
        self.aft_temp_frame.grid(row=2, column=0)
        self.aft_def_label = tk.Label(self.after_tomorrow_lb, text=(self.daily_forcast[1]['description']), font=self.data_font, anchor='c')
        self.aft_def_label.grid(row=0, column=0)
        self.aft_min_temp_label = tk.Label(self.aft_temp_frame, text=('Min: %s cel.' % (self.daily_forcast[1]['min'])), font=self.data_font)
        self.aft_min_temp_label.grid(row=0, column=0, padx=40)
        self.aft_max_temp_label = tk.Label(self.aft_temp_frame, text=('Max: %s cel.' % (self.daily_forcast[1]['max'])), font=self.data_font)
        self.aft_max_temp_label.grid(row=1, column=0)
        # In Two Days
        self.twodays_icon_img = self.forcast.forcast_icon(self.daily_forcast[2]['icon'])
        self.twodays_icon_label = tk.Label(self.two_days_lb, image=self.twodays_icon_img, bg='grey88', anchor='nw')
        self.twodays_icon_label.grid(row=1, column=0, sticky='n')
        self.twodays_temp_frame = tk.Frame(self.two_days_lb)
        self.twodays_temp_frame.grid(row=2, column=0)
        self.twodays_def_label = tk.Label(self.two_days_lb, text=(self.daily_forcast[2]['description']), font=self.data_font, anchor='c')
        self.twodays_def_label.grid(row=0, column=0)
        self.twodays_min_temp_label = tk.Label(self.twodays_temp_frame, text=('Min: %s cel.' % (self.daily_forcast[2]['min'])), font=self.data_font)
        self.twodays_min_temp_label.grid(row=0, column=0, padx=40)
        self.twodays_max_temp_label = tk.Label(self.twodays_temp_frame, text=('Max: %s cel.' % (self.daily_forcast[2]['max'])), font=self.data_font)
        self.twodays_max_temp_label.grid(row=1, column=0)
    
    def forcast_update(self):
        self.f_canvas.destroy()
        self.forecast()




if __name__ == "__main__":
    # Calculating RunTime
    startTime = time.time()
    print('T.time:', startTime)
    
    
    # App start
    root = Root()
    root.forecast()
    root.widgets()
    root.forcast_graph()
    root.mainloop()

    # Calculating RunTime
    endTime = time.time() 
    print('E.time::', endTime)
    proccess_length = endTime - startTime
    print('P.time:', proccess_length)
    #end_process_time = time.process_time_ns()
    #process_delta = time.localtime(end_process_time - start_process_time)
    #print(process_total)