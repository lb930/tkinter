from tkinter import *
import time
from tkinter import messagebox

class Application(Frame):
    def __init__(self,master):
        super(Application,self).__init__(master)
        self.place()
        self.widgets()
        self.running = False

    def widgets(self):
        root.geometry('245x150')
        # Background colour
        root.configure(bg='#11375c')

        # Entry fields
        self.hour = StringVar()
        self.hour.set("00")
        self.hour_entry = Entry(width = 2, font=("Calibri",34,""), textvariable = self.hour, bg = '#11375c', fg = '#ffffff', relief = 'flat')
        self.hour_entry.place(x = 28, y = 10)

        self.minute = StringVar()
        self.minute.set("00")
        self.minute_entry = Entry(width = 2, font=("Calibri",34), textvariable = self.minute, bg = '#11375c', fg = '#ffffff', relief = 'flat')
        self.minute_entry.place(x = 98, y = 10)

        self.second = StringVar()
        self.second.set("00")
        self.seconds_entry = Entry(width = 2, font=("Calibri",34), textvariable = self.second, bg = '#11375c', fg = '#ffffff', relief = 'flat')
        self.seconds_entry.place(x = 168, y = 10)

        # Labels
        colon_1 = Label(text = ':', font=("Calibri",34,""), bg = '#11375c', fg = '#ffffff')
        colon_1.place(x = 78, y = 7)

        colon_2 = Label(text = ':', font=("Calibri",34,""), bg = '#11375c', fg = '#ffffff')
        colon_2.place(x = 148, y = 7)

        # Buttons
        self.start_btn = Button(text = "Start", command=self.start, height = 2, width = 6, bg = '#6eeb94', font=("Calibri", 11))
        self.start_btn.place(x = 95, y = 79)

        self.stop_btn = Button(text = "Stop", command=self.stop, height = 2, width = 6, font=("Calibri", 11))
        self.stop_btn.place(x = 25, y = 79)

        self.reset_btn = Button(text = "Reset", command=self.reset, height = 2, width = 6, font=("Calibri", 11))
        self.reset_btn.place(x = 165, y = 79)

    def clock(self):
        if self.running == True:
            
            # returns 3600/60 = 60 with 0 left: so that's 60 min, 0 seconds
            self.mins, self.secs = divmod(self.time_total,60) 

            self.hours = 0
            if self.mins > 60:
                self.hours, self.mins = divmod(self.mins, 60)

            self.hour.set("{0:02d}".format(self.hours))
            self.minute.set("{0:02d}".format(self.mins))
            self.second.set("{0:02d}".format(self.secs))

            root.update()
            root.after(1000, self.clock)  # wait 1 second, re-call clock

            if self.time_total == 0:
                self.running = False
                messagebox.showinfo("Time Countdown", "Time's up!")
            self.time_total -= 1
                    
    def start(self):
        self.time_total = int(self.hour_entry.get())*3600 + int(self.minute_entry.get())*60 + int(self.seconds_entry.get())
        self.running = True
        self.clock()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.hour.set("00")
        self.minute.set("00")
        self.second.set("00")
    
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.title('Timer')
    mainloop()