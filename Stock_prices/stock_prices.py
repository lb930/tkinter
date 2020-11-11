from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
import json
import requests
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StockApp(Frame):
    def __init__(self, master):
        super(StockApp, self).__init__(master)
        self.place()
        self.widgets()

    def widgets(self):
        # width * height
        root.geometry('510x450')
        root.configure(bg='#FFFFFF')

        # Header
        border_top = Label(text='_______', font=('Calibri light', 24, ''), bg='#FFFFFF')
        border_top.place(x=30, y=0)
        
        border_bottom = Label(text='_______', font=('Calibri light', 24, ''), bg='#FFFFFF')
        border_bottom.place(x=350, y=0)
        
        header_label = Label(text='STOCK PRICES', font=('Calibri light', 24, ''), bg='#FFFFFF')
        header_label.place(x=157, y=15)

        # Enter your API key
        api_key_label = Label(text='API key', font=('Calibri', 10), bg='#FFFFFF')
        api_key_label.place(x=30, y=80)

        self.api_key_field = Entry(width=32, font=('Calibri', 10), bg='#F4F4F4')
        self.api_key_field.config(show="*")
        self.api_key_field.place(x=30, y=105)

        # Enter an index
        index_label = Label(text='Stock index', font=('Calibri', 10), bg='#FFFFFF')
        index_label.place(x=275, y=80)

        self.index_field = Entry(width=19, font=('Calibri', 10), bg='#F4F4F4')
        self.index_field.place(x=275, y=105)

        # OK button
        ok_btn = Button(text='OK', command=self.ok, font=('Calibri', 8), bg='#F4F4F4', width=5)
        ok_btn.place(x=430, y=103)
        
        # Symbol
        self.symbol_var = StringVar()
        self.symbol_label = Label(textvariable = self.symbol_var, font=('Calibri', 14, 'bold'), bg = '#FFFFFF', fg='#000000')
        self.symbol_var.set('')
        self.symbol_label.place(x = 50, y = 145)
        
        # Exchange
        self.exchange_var = StringVar()
        self.exchange_label = Label(textvariable = self.exchange_var, font=('Calibri', 9), bg = '#FFFFFF', fg='#6b6969')
        self.exchange_var.set('')
        self.exchange_label.place(x = 50, y = 169)
        
        # Last adjusted close
        self.last_close_var = StringVar()
        self.last_close_label = Label(textvariable = self.last_close_var, font=('Calibri', 18), bg = '#FFFFFF', fg='#000000')
        self.last_close_var.set('')
        self.last_close_label.place(x = 400, y = 155)


    def call_api(self):
        
        if len(self.api_key_field.get()) == 0:
            raise ValueError('Please provide a valid API key')
        elif len(self.index_field.get()) == 0:
            raise ValueError('Please provide a valid stock index')
        else:
            url  = requests.get(f'http://api.marketstack.com/v1/eod?access_key={self.api_key_field.get()}&symbols={self.index_field.get()}&limit=1000')
            current_stock = json.loads(url.text)

            self.symbol = current_stock['data'][0]['symbol']
            self.exchange = current_stock['data'][0]['exchange']
            self.adj_close_latest = current_stock['data'][0]['adj_close']
            self.df = pd.DataFrame(current_stock['data'])
        
    def format_df(self):

        self.df['date'] = self.df['date'].str[:10]
        self.df['date'] = pd.to_datetime(self.df['date'])

        self.df = self.df[['date', 'adj_close']]
        self.df.set_index('date', inplace = True)

    def draw_chart(self):

        fig, ax = plt.subplots(figsize=(5,2.5), dpi=100)
        self.df.plot(ax=ax, linewidth=0.2)
        
        ax.fill_between(x = self.df.index.values, y1 = self.df['adj_close'], color="skyblue", alpha=0.4)

        # #set major ticks format
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # Remove axes and change colour
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#9c9ea1')
        ax.xaxis.label.set_color('#9c9ea1')
        ax.tick_params(axis='both', colors='#9c9ea1', labelsize = 8)

        
        # Horizotal grid lines
        ax.grid(axis='y', linestyle='--', linewidth = 0.4, color = '#edeef0')
        
        # Remove legend
        ax.get_legend().remove()
        
        # Add to tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw() # TK-Drawingarea
        canvas.get_tk_widget().place(x = 20, y = 185)
        canvas._tkcanvas.place(x = 20, y = 185)
        
    def update_labels(self):
        
        self.symbol_var.set(self.symbol)
        self.exchange_var.set(self.exchange)
        self.last_close_var.set(self.adj_close_latest)
        
        root.update()

    def ok(self):
        self.call_api()
        self.format_df()
        self.draw_chart()
        self.update_labels()
        
if __name__ == "__main__":
    root= Tk()
    app= StockApp(root)
    root.title('Stock prices')
    mainloop()
