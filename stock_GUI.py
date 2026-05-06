# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("Ethan Stock Manager")
        self.root.geometry("600x750")
        self.root.resizable(True, True)
        self.root.configure(bg="#2b2b2b")

        # Add Menubar
        self.menubar = Menu(self.root, bg="#3c3f41", fg="white", activebackground="#4c5052", activeforeground="white")

        # Add File Menu
        self.filemenu = Menu(self.menubar, tearoff=0, bg="#3c3f41", fg="white", activebackground="#4c5052", activeforeground="white")
        self.filemenu.add_command(label="Load", command=self.load)
        self.filemenu.add_command(label="Save", command=self.save)

        # Add Web Menu
        self.webmenu = Menu(self.menubar, tearoff=0, bg="#3c3f41", fg="white", activebackground="#4c5052", activeforeground="white")
        self.webmenu.add_command(label="Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label="Import CSV from Yahoo! Finance...", command=self.importCSV_web_data)

        # Add Chart Menu
        self.chartmenu = Menu(self.menubar, tearoff=0, bg="#3c3f41", fg="white", activebackground="#4c5052", activeforeground="white")
        self.chartmenu.add_command(label="Show Chart", command=self.display_chart)

        # Add menus to window
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Web", menu=self.webmenu)
        self.menubar.add_cascade(label="Chart", menu=self.chartmenu)
        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(
            self.root,
            text="Ethan's Stock Manager",
            font=("Arial", 16, "bold"),
            bg="#495c6c",
            fg="white",
            pady=6
        )
        self.headingLabel.pack(fill=X)

        self.mainFrame = Frame(self.root, bg="#2b2b2b")
        self.mainFrame.pack(fill=BOTH, expand=True, padx=8, pady=8)

        # Add stock list
        stockListFrame = Frame(self.mainFrame, bg="#2b2b2b")
        stockListFrame.pack(side=RIGHT, fill=Y, padx=(8, 0))

        Label(stockListFrame, text="Stock List", font=("Arial", 10, "bold"), bg="#2b2b2b", fg="#bbbbbb").pack(anchor=W)

        listScroll = Scrollbar(stockListFrame)
        listScroll.pack(side=RIGHT, fill=Y)

        self.stockList = Listbox(
            stockListFrame,
            height=20,
            width=20,
            yscrollcommand=listScroll.set,
            bg="#3c3f41",
            fg="white",
            selectbackground="#1e88e5",
            selectforeground="white",
            font=("Courier", 11),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#1e88e5"
        )
        self.stockList.pack(side=LEFT, fill=Y)
        listScroll.config(command=self.stockList.yview)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        # Add Tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background="#2b2b2b", borderwidth=0)
        style.configure("TNotebook.Tab", background="#3c3f41", foreground="#bbbbbb", padding=[12, 5], font=("Arial", 10))
        style.map("TNotebook.Tab", background=[("selected", "#1e88e5")], foreground=[("selected", "white")])

        self.tabControl = ttk.Notebook(self.mainFrame)
        self.tabControl.pack(side=LEFT, expand=True, fill=BOTH)

        self.mainTab = Frame(self.tabControl, bg="#2b2b2b")
        self.historyTab = Frame(self.tabControl, bg="#2b2b2b")
        self.reportTab = Frame(self.tabControl, bg="#2b2b2b")

        self.tabControl.add(self.mainTab, text="  Main  ")
        self.tabControl.add(self.historyTab, text="  History  ")
        self.tabControl.add(self.reportTab, text="  Report  ")

        # Set Up Main Tab
        centerFrame = Frame(self.mainTab, bg="#2b2b2b")
        centerFrame.pack(expand=True, anchor=CENTER)

        # add stock section
        addFrame = LabelFrame(
            centerFrame,
            text="Add Stock",
            font=("Arial", 10),
            bg="#2b2b2b",
            fg="#D3D3D3",
            padx=10,
            pady=5
        )
        addFrame.grid(row=0, column=0, padx=14, pady=(14, 6))

        Label(addFrame, text="Ticker Symbol:", bg="#2b2b2b", fg="#dddddd", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=4)
        self.addSymbolEntry = Entry(addFrame, width=18, bg="#3c3f41", fg="white", font=("Arial", 10))
        self.addSymbolEntry.grid(row=0, column=1, padx=(8, 0), pady=4)

        Label(addFrame, text="Company Name:", bg="#2b2b2b", fg="#dddddd", font=("Arial", 10)).grid(row=1, column=0, sticky=W, pady=4)
        self.addNameEntry = Entry(addFrame, width=18, bg="#3c3f41", fg="white", font=("Arial", 10))
        self.addNameEntry.grid(row=1, column=1, padx=(8, 0), pady=4)

        Label(addFrame, text="Shares:", bg="#2b2b2b", fg="#dddddd", font=("Arial", 10)).grid(row=2, column=0, sticky=W, pady=4)
        self.addSharesEntry = Entry(addFrame, width=18, bg="#3c3f41", fg="white", font=("Arial", 10))
        self.addSharesEntry.grid(row=2, column=1, padx=(8, 0), pady=4)

        Button(
            addFrame,
            text="Add Stock",
            command=self.add_stock,
            bg="#c0c0c0",
            fg="#2b2b2b",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=4,
        ).grid(row=3, column=0, columnspan=2, pady=(8, 2))

        # update shares (buy/sell)
        updateFrame = LabelFrame(
            centerFrame,
            text="Update Shares",
            font=("Arial", 10),
            bg="#2b2b2b",
            fg="#D3D3D3",
            padx=6,
            pady=8
        )
        updateFrame.grid(row=1, column=0, padx=14, pady=8)

        Label(updateFrame, text="Shares:", bg="#2b2b2b", fg="#dddddd", font=("Arial", 10)).grid(row=0, column=0, sticky=W, pady=4)
        self.updateSharesEntry = Entry(updateFrame, width=18, bg="#3c3f41", fg="white", font=("Arial", 10))
        self.updateSharesEntry.grid(row=0, column=1, padx=(8, 0), pady=4)

        Button(updateFrame, text="Buy", command=self.buy_shares, bg="#c0c0c0", fg="#2b2b2b", font=("Arial", 10, "bold"), padx=10, pady=3).grid(row=1, column=0, padx=4, pady=(8,2))
        Button(updateFrame, text="Sell", command=self.sell_shares, bg="#c0c0c0", fg="#2b2b2b", font=("Arial", 10, "bold"), padx=10, pady=3).grid(row=1, column=1, padx=4, pady=(8,2))
        Button(updateFrame, text="Delete Stock", command=self.delete_stock, bg="#c0c0c0", fg="#2b2b2b", font=("Arial", 10), padx=6, pady=3).grid(row=2, column=0, columnspan=2, pady=(4,2))


        # get data from yahoo finance
        dataFrame = LabelFrame(
            centerFrame,
            text="Get Data",
            font=("Arial", 10),
            bg="#2b2b2b",
            fg="#D3D3D3",
            padx=8,
            pady=4
        )
        dataFrame.grid(row=2, column=0, padx=14, pady=8)

        Button(
            dataFrame,
            text="Scrape Data from Yahoo! Finance",
            command=self.scrape_web_data,
            bg="#c0c0c0",
            fg="#2b2b2b",
            font=("Arial", 10),
            padx=8,
            pady=4,
        ).pack(fill=X, pady=(0, 6))

        Button(
            dataFrame,
            text="Import CSV from Yahoo! Finance",
            command=self.importCSV_web_data,
            bg="#c0c0c0",
            fg="#2b2b2b",
            font=("Arial", 10),
            padx=8,
            pady=4,
        ).pack(fill=X, pady=(0, 6))

        Button(
            dataFrame,
            text="Show Chart",
            command=self.display_chart,
            bg="#c0c0c0",
            fg="#2b2b2b",
            font=("Arial", 10),
            padx=8,
            pady=4,
        ).pack(fill=X)

        # Setup History Tab
        Label(self.historyTab, text="Price & Volume History", font=("Arial", 11, "bold"), bg="#2b2b2b", fg="#D3D3D3").pack(anchor=W, padx=12, pady=(10, 4))

        historyFrame = Frame(self.historyTab, bg="#2b2b2b")
        historyFrame.pack(fill=BOTH, expand=True, padx=12, pady=(0, 12))

        historyScroll = Scrollbar(historyFrame)
        historyScroll.pack(side=RIGHT, fill=Y)

        self.dailyDataList = Text(
            historyFrame,
            yscrollcommand=historyScroll.set,
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=("Courier", 10),
            
            padx=8,
            pady=8,
        )
        self.dailyDataList.pack(side=LEFT, fill=BOTH, expand=True)
        historyScroll.config(command=self.dailyDataList.yview)

        # Setup Report Tab
        Label(self.reportTab, text="Stock Report", font=("Arial", 11, "bold"), bg="#2b2b2b", fg="#D3D3D3").pack(anchor=W, padx=12, pady=(10, 4))

        reportFrame = Frame(self.reportTab, bg="#2b2b2b")
        reportFrame.pack(fill=BOTH, expand=True, padx=12, pady=(0, 12))

        reportScroll = Scrollbar(reportFrame)
        reportScroll.pack(side=RIGHT, fill=Y)

        self.stockReport = Text(
            reportFrame,
            yscrollcommand=reportScroll.set,
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=("Courier", 10),
            
            padx=8,
            pady=8,
        )
        self.stockReport.pack(side=LEFT, fill=BOTH, expand=True)
        reportScroll.config(command=self.stockReport.yview)

        ## Call MainLoop
        self.root.mainloop()

# This section provides the functionality

    # loads stocks from the database into the list
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # saves everything to the database
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # called when user clicks a stock in the list
    def update_data(self, evt):
        self.display_stock_data()

    # fills in the history and report tabs for the selected stock
    def display_stock_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = "Ethan's Stock Manager"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                self.dailyDataList.insert(END,"- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)

                #display report
                self.stockReport.insert(END, "Stock Report ---\n")
                self.stockReport.insert(END, "Report for:  " + stock.symbol + " " + stock.name + "\n")
                self.stockReport.insert(END, "Shares:  " + str(stock.shares) + "\n\n")
                if len(stock.DataList) == 0:
                    self.stockReport.insert(END, "*** No daily history.\n")
                else:
                    self.stockReport.insert(END, f"{'Date':<12}{'Close Price'}\n")
                    self.stockReport.insert(END, "=" * 25 + "\n")
                    for daily_data in stock.DataList:
                        date_str = daily_data.date.strftime("%m/%d/%y")
                        price_str = '${:0,.2f}'.format(daily_data.close)
                        report_row = f"{date_str:<12}{price_str}\n"
                        self.stockReport.insert(END, report_row)
                    self.stockReport.insert(END, "\n--- Report Complete ---\n")

    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(),self.addNameEntry.get(),float(str(self.addSharesEntry.get())))
        self.stock_list.append(new_stock)
        self.stockList.insert(END,self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    # buys shares for whichever stock is selected
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = "Ethan's Stock Manager"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # same as buy but subtracts instead
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = "Ethan Stock Manager"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # removes the stock and all its data
    def delete_stock(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.remove(stock)
                self.stockList.delete(self.stockList.curselection())
                self.headingLabel['text'] = "Ethan Stock Manager"
                messagebox.showinfo("Delete Stock", symbol + " Deleted")
                return

    # pulls data from yahoo finance using selenium
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (mm/dd/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (mm/dd/yy")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # lets user pick a csv file and imports the data
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + "Import Complete")

    # shows the price chart for the selected stock
    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list,symbol)


def main():
        app = StockApp()


if __name__ == "__main__":
    # execute only if run as a script
    main()