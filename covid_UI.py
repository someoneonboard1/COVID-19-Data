from data_collector import collection_local, collection_us, collection_global #These are the imports from the other programs
import tkinter as tk #Used to make the GUI
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
import datetime #Used to show the update time when the program runs


matplotlib.use("TkAgg")  # The backend of matplotlib and how it is used
style.use("fivethirtyeight") #Can also use 'classic' if preferred


global_data = collection_global() #The next three lines create the dictionary from the data creating functions
local_data = collection_local()
us_data = collection_us()


class CovidData(tk.Tk):  # Inheriting from the tkinter library
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # Tkinter is also being initialized
        root = tk.Frame(self) #root is a frame that goes within the main, which is self
        self.title("COVID-19 Data")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        root.pack(side="top", fill="both",expand=True)  # Fill is used to fill in alloted space, expand is used for any whitespace is left to fill it in

        root.grid_rowconfigure(0,weight=1)  # 0 is the minimum size of it, weight is used to dictate the prioritization of them, since both are 1 they have equal prioritization
        root.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Frame will be kept in this, will be used to move between the frames/windows

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(root, self) #they go within the parent which is named root

            self.frames[F] = frame #this instance of the class is then added to the dictionary

            frame.grid(row=0, column=0,sticky="nsew")  # sticky is used to align and stretch everything in all four directions. nsew stands for north, south, east, west

        self.show_frame(StartPage)  # When initialized, the start page will be what we see first

    def show_frame(self, cont):  # Cont is the key
        frame = self.frames[cont]  # frame is the value that cont corresponds to
        frame.tkraise()  # This raises the window that we want to the front of the frame


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        now = datetime.datetime.now()
        tk.Frame.__init__(self, parent)  # The parent arg is the class that we've created above that we use
        title = tk.Label(self, text="COVID-19 Data", font="times 20 bold")
        title.pack()
        stamp = tk.Label(self, text=f"Updated as of {now.strftime('%d-%m-%y at (%H:%M)')}")
        stamp.pack(pady=30)

        button1 = tk.Button(self, text="Global Data", command=lambda: controller.show_frame(PageOne))
        button1.pack(pady=10) #lambda is a throwaway function that allows us to move to the different pages using the show_frame function

        button2 = tk.Button(self, text="US Data", command=lambda: controller.show_frame(PageTwo))
        button2.pack(pady=10)

        button2 = tk.Button(self, text="Florida Data", command=lambda: controller.show_frame(PageThree))
        button2.pack(pady=10)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Global COVID-19 Data", font="times 16 bold")
        title.pack(pady=10)

        button = tk.Button(self, text="Home Page", command=lambda: controller.show_frame(StartPage))
        button.pack(pady=10)

        f = Figure(figsize=(1, 1), dpi=100)
        ax1 = f.add_subplot(211) # Height, width, plot number
        ax2 = f.add_subplot(223)
        ax3 = f.add_subplot(224)


        ax1.set_title(f"GLOBAL DATA\nTotal Cases: {global_data.get('cases')}")
        labels = [f"Active Cases - {global_data.get('active_infected')}",
                  f"Closed Cases - {global_data.get('closed_case')}"]
        slices = [int(global_data.get('active_infected')), int(global_data.get('closed_case'))]
        ax1.pie(slices, labels=labels, autopct="%1.1f%%", textprops={'fontsize': 8})


        ax2.set_title(f"Total Closed Cases: {global_data.get('closed_case')}")
        labels = [f"Recovered - {global_data.get('recovered')}",
                  f"Dead - {global_data.get('deaths')}"]
        slices = [int(global_data.get('recovered')), int(global_data.get('deaths'))]
        ax2.pie(slices, labels=labels, autopct="%1.1f%%", textprops={'fontsize': 8})


        ax3.set_title(f"Total Active Cases: {global_data.get('active_infected')}")
        labels = [f"Mild - {global_data.get('mild')}",
                  f"Serious - {global_data.get('serious')}"]
        slices = [int(global_data.get('mild')), int(global_data.get('serious'))]
        ax3.pie(slices, labels=labels, autopct="%1.1f%%", textprops={'fontsize': 8})


        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="US COVID-19 Data", font="times 16 bold")
        title.pack(pady=10)

        button = tk.Button(self, text="Home Page", command=lambda: controller.show_frame(StartPage))
        button.pack(pady=10)

        f = Figure(figsize=(1, 1), dpi=100)
        ax1 = f.add_subplot(211)  # Height, width, plot number
        ax2 = f.add_subplot(223)
        ax3 = f.add_subplot(224)


        ax1.set_title(f"US DATA\nTotal Cases: {us_data.get('cases')}")
        labels = [f"Active Cases - {us_data.get('active_infected')}",
                  f"Closed Cases - {us_data.get('closed_case')}"]
        slices = [int(us_data.get('active_infected')), int(us_data.get('closed_case'))]
        ax1.pie(slices, labels=labels, autopct="%1.1f%%", textprops={'fontsize': 8})


        ax2.set_title(f"Total Closed Cases: {us_data.get('closed_case')}")
        labels = [f"Recovered - {us_data.get('recovered')}",
                  f"Dead - {us_data.get('deaths')}"]
        slices = [int(us_data.get('recovered')), int(us_data.get('deaths'))]
        ax2.pie(slices, labels=labels, autopct="%1.1f%%", textprops={'fontsize': 8})


        ax3.set_title(f"Total Active Cases: {us_data.get('active_infected')}")
        labels = [f"Mild - {us_data.get('mild')}",
                  f"Serious - {us_data.get('serious')}"]
        slices = [int(us_data.get('mild')), int(us_data.get('serious'))]
        ax3.pie(slices, labels=labels, autopct="%1.1f%%", textprops={'fontsize': 8})


        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title = tk.Label(self, text="Florida COVID-19 Data", font="times 16 bold")
        title.pack(pady=10)

        button = tk.Button(self, text="Home Page", command=lambda: controller.show_frame(StartPage))
        button.pack(pady=10)

        f = Figure(figsize=(1, 1), dpi=100)
        ax1 = f.add_subplot(111)


        ax1.set_title(f"Total Florida Cases: {local_data.get('total')}")
        slices = [int(local_data.get('cases_residents')), int(local_data.get('cases_non'))]
        labels = [f"Residents - {local_data.get('cases_residents')}", f"Non-Residents - {local_data.get('cases_non')}"]
        ax1.pie(slices, labels=labels, autopct="%1.1f%%", textprops={'fontsize': 8})

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = CovidData()
app.mainloop()