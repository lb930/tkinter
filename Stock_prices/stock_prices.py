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
        root.geometry('500x400')
        root.configure(bg='#FFFFFF')

        # Header
        header_label = Label(text='Stock Prices', font=(
            'Calibri', 22, 'bold'), bg='#FFFFFF')
        header_label.place(x=30, y=15)

        # Enter your API key
        api_key_label = Label(text='API key', font=(
            'Calibri', 10), bg='#FFFFFF')
        api_key_label.place(x=30, y=65)

        self.api_key_field = Entry(
            width=32, font=('Calibri', 10), bg='#F4F4F4')
        self.api_key_field.config(show="*")
        self.api_key_field.place(x=30, y=90)

        # Enter an index
        index_label = Label(text='Stock index', font=(
            'Calibri', 10), bg='#FFFFFF')
        index_label.place(x=280, y=65)

        self.index_field = Entry(width=15, font=('Calibri', 10), bg='#F4F4F4')
        self.index_field.place(x=280, y=90)

        # OK button
        ok_btn = Button(text='OK', command=self.ok, font=(
            'Calibri', 8), bg='#F4F4F4', width=5)
        ok_btn.place(x=400, y=88)

    def call_api(self):
        ######## change API key and symbol once done ##############
        # url  = requests.get(f'http://api.marketstack.com/v1/eod?access_key=996a4bf6ea79afe82bef5078dfcb1ac7&symbols=AAPL&limit=1000')
        # current_stock = json.loads(url.text)

        current_stock = {'pagination': {'limit': 100, 'offset': 0, 'count': 100, 'total': 251
    }, 'data': [
        {'open': 118.32, 'high': 119.2, 'low': 116.13, 'close': 118.69, 'volume': 114457922.0, 'adj_high': 119.2, 'adj_low': 116.13, 'adj_close': 118.69, 'adj_open': 118.32, 'adj_volume': 114457922.0, 'symbol': 'AAPL', 'exchange': 'XNAS', 'date': '2020-11-06T00: 00: 00+0000'
        },
        {'open': 117.95, 'high': 119.62, 'low': 116.8686, 'close': 119.03, 'volume': 126387074.0, 'adj_high': 119.4137499474, 'adj_low': 116.66709394, 'adj_close': 118.8247672316, 'adj_open': 117.7466293789, 'adj_volume': 126387074.0, 'symbol': 'AAPL', 'exchange': 'XNAS', 'date': '2020-11-05T00: 00: 00+0000'
        },
        {'open': 114.14, 'high': 115.59, 'low': 112.35, 'close': 114.95, 'volume': 138235482.0, 'adj_high': 115.59, 'adj_low': 112.35, 'adj_close': 114.95, 'adj_open': 114.14, 'adj_volume': 138235482.0, 'symbol': 'AAPL', 'exchange': 'XNAS', 'date': '2020-11-04T00: 00: 00+0000'
        },
        {'open': 109.66, 'high': 111.49, 'low': 108.73, 'close': 110.44, 'volume': 107624448.0, 'adj_high': 111.49, 'adj_low': 108.73, 'adj_close': 110.44, 'adj_open': 109.66, 'adj_volume': 107624448.0, 'symbol': 'AAPL',
    'exchange': 'XNAS', 'date': '2020-11-03T00: 00: 00+0000'
        }]}

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

        #plot data
        fig, ax = plt.subplots(figsize=(2,1), dpi=50)
        self.df.plot(ax=ax)

        # #set major ticks format
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.get_legend().remove()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw() # TK-Drawingarea
        # Do I need to place both?
        canvas.get_tk_widget().place(x = 30, y = 150)
        canvas._tkcanvas.place(x = 30, y = 150)

    def ok(self):
        self.call_api()
        self.format_df()
        self.draw_chart()


if __name__ == "__main__":
    root= Tk()
    app= StockApp(root)
    root.title('Stock prices')
    mainloop()
