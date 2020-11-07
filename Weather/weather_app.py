import json
import requests
from tkinter import *
from PIL import Image, ImageTk

class Weather(Frame):
    def __init__(self, master):
        super(Weather, self).__init__(master)
        self.place()
        self.widgets()

    def widgets(self):
        # width * height
        root.geometry('260x400')
        root.configure(bg='#2d0f59')

        # Enter your API key
        api_key_label = Label(text='API key', font=('Calibri', 10), fg = '#FFFFFF', bg='#2d0f59')
        api_key_label.place(x=15, y=20)

        self.api_key_field = Entry(width=22, font=('Calibri', 10))
        self.api_key_field.config(show="*")
        self.api_key_field.place(x=80, y=20)

        # Enter a location
        location_label = Label(text='Location', font=('Calibri', 10), fg = '#FFFFFF', bg='#2d0f59')
        location_label.place(x=15, y=51)

        self.location_field = Entry(width=15, font=('Calibri', 10))
        self.location_field.place(x=80, y=51)

        # OK button
        ok_btn = Button(text='Go!', command=self.go, font=('Calibri', 10), fg = '#000000', bg='#f7f7f7', width = 4)
        ok_btn.place(x=201, y=48)

        # Current weather description
        self.weather_desc_var = StringVar()
        self.weather_desc_label = Label(textvariable=self.weather_desc_var, font=('Calibri', 11), fg = '#FFFFFF', bg='#2d0f59')
        self.weather_desc_var.set('')
        self.weather_desc_label.place(x=130, y=113, anchor = 'center')

        # Current temperature
        self.current_temp_var = StringVar()
        self.current_temp_label = Label(textvariable=self.current_temp_var, font=('Calibri', 40), fg = '#FFFFFF', bg='#2d0f59')
        self.current_temp_var.set('')
        self.current_temp_label.place(x=130, y=157, anchor = 'center')

        # Current location
        self.current_location_var = StringVar()
        self.current_location_label = Label(textvariable=self.current_location_var, font=('Calibri', 11), fg = '#FFFFFF', bg='#2d0f59')
        self.current_location_var.set('')
        self.current_location_label.place(x=130, y=200, anchor = 'center')

        # Unit
        self.unit_var = StringVar()
        self.unit_label = Label(textvariable = self.unit_var, font = ('Calibri', 11, 'bold'), fg = '#FFFFFF', bg='#2d0f59')
        self.unit_var.set('')
        self.unit_label.place(x=158, y=131)

        ### Feels like ###
        # Header
        self.feels_like_header_var = StringVar()
        self.feels_like_header_label = Label(textvariable = self.feels_like_header_var, font=('Calibri', 10), fg = '#FFFFFF', bg='#2d0f59')
        self.feels_like_header_var.set('')
        self.feels_like_header_label.place(x = 25, y = 240)

        #Value
        self.feels_like_var = StringVar()
        self.feels_like_label = Label(textvariable=self.feels_like_var, font=('Calibri', 10), fg = '#FFFFFF', bg='#2d0f59')
        self.feels_like_var.set('')
        self.feels_like_label.place(x=35, y=315)

        ### Humidity ###
        # Header
        self.humidity_header_var = StringVar()
        self.humidity_header_label = Label(textvariable = self.humidity_header_var, font=('Calibri', 10), fg = '#FFFFFF', bg='#2d0f59')
        self.humidity_header_var.set('')
        self.humidity_header_label.place(x = 105, y = 240)

        #Value
        self.humidity_var = StringVar()
        self.humidity_label = Label(textvariable=self.humidity_var, font=('Calibri', 10), fg = '#FFFFFF', bg='#2d0f59')
        self.humidity_var.set('')
        self.humidity_label.place(x=117, y=315)

        ### Wind ###
        # Header
        self.wind_header_var = StringVar()
        self.wind_header_label = Label(textvariable = self.wind_header_var, font=('Calibri', 10), fg = '#FFFFFF', bg='#2d0f59')
        self.wind_header_var.set('')
        self.wind_header_label.place(x = 192, y = 240)

        # Value
        self.wind_var = StringVar()
        self.wind_label = Label(textvariable=self.wind_var, font=('Calibri', 10), fg = '#FFFFFF', bg='#2d0f59')
        self.wind_var.set('')
        self.wind_label.place(x=183, y=315)

        # Source
        source_label = Label(text = 'Data provided by weatherstack.com', font=('Calibri', 8), fg = '#FFFFFF', bg='#2d0f59')
        source_label.place(x = 15, y = 365)

    def get_data(self):

        if len(self.api_key_field.get()) == 0:
            raise ValueError('Please provide a valid API key')

        url_current = f'http://api.weatherstack.com/current?access_key={self.api_key_field.get()}&query={self.location_field.get()}&unit=m'
        json_url_current = requests.get(url_current)
        current_weather = json.loads(json_url_current.text)

        self.location = current_weather['location']['name']
        self.temperature_now = current_weather['current']['temperature']
        self.weather_desc = current_weather['current']['weather_descriptions'][0]

        self.feels_like = str(current_weather['current']['feelslike'])+'°C'
        self.humidity = str(current_weather['current']['humidity'])+'%'
        self.wind = str(current_weather['current']['wind_speed'])+' km/h'

        self.update_labels()

    def update_labels(self):
        
        # Current weather
        self.weather_desc_var.set(self.weather_desc)
        self.current_temp_var.set(self.temperature_now)
        self.current_location_var.set(self.location)
        self.unit_var.set('°C')

        # Feels like
        self.feels_like_header_var.set('Feels like')
        self.feels_like_var.set(self.feels_like)

        self.Feels_image = Image.open('weather.png')
        self.Feels_image_render = ImageTk.PhotoImage(self.Feels_image)
        canvas_Feels = Canvas(bg='#2d0f59', width=47, height=40, bd=0, highlightthickness=0, relief='ridge')
        canvas_Feels.create_image(24, 22, image=self.Feels_image_render)
        canvas_Feels.place(x=27, y=268)

        # Humidity
        self.humidity_header_var.set('Humidity')
        self.humidity_var.set(self.humidity)

        self.humidity_image = Image.open('humidity.png')
        self.humidity_image_render = ImageTk.PhotoImage(self.humidity_image)
        canvas_humid = Canvas(bg='#2d0f59', width=44, height=40, bd=0, highlightthickness=0, relief='ridge')
        canvas_humid.create_image(24, 22, image=self.humidity_image_render)
        canvas_humid.place(x=105, y=265)

        # Wind speed
        self.wind_header_var.set('Wind')
        self.wind_var.set(self.wind)

        self.wind_image = Image.open('wind.png')
        self.wind_image_render = ImageTk.PhotoImage(self.wind_image)
        canvas_wind = Canvas(bg='#2d0f59', width=44, height=40, bd=0, highlightthickness=0, relief='ridge')
        canvas_wind.create_image(24, 22, image=self.wind_image_render)
        canvas_wind.place(x=183, y=265)

        root.update()
        
    def go(self):
        self.get_data()

if __name__ == '__main__':
    root = Tk()
    app = Weather(root)
    root.title('Weather')
    mainloop()
