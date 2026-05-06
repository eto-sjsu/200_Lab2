# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

def add_stock(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Add Stock ---")
        symbol = input("Enter Ticker Symbol: ")
        name = input("Enter Company Name: ")
        shares = float(input("Enter Number of Shares: "))
        new_stock = Stock(symbol, name, shares)
        stock_list.append(new_stock)
        option = input("Stock Added - Enter to Add Another Stock or 0 to Stop: ")
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")
        while option not in ["1", "2", "0"]:
            clear_screen()
            print("Invalid Option")
            print("1 - Buy Shares")
            print("2 - Sell Shares")
            print("0 - Exit Update Shares")
            option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        else:
            print("Returning to Manage Stocks")


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    symbols = [s.symbol for s in stock_list]
    print("Stocks:", symbols)
    symbol = input("Which stock do you want to buy?: ")
    for stock in stock_list:
        if stock.symbol == symbol:
            amount = float(input("How many shares do you want to buy?: "))
            stock.buy(amount)
            print("Purchased")
            input("Press Enter to Continue")
            return
    print("Stock not found")
    input("Press Enter to Continue")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    for stock in stock_list:
        print(" -", stock.symbol)
    symbol = input("Which stock do you want to sell?: ")
    for stock in stock_list:
        if stock.symbol == symbol:
            amount = float(input("How many shares do you want to sell?: "))
            stock.sell(amount)
            print("Sold")
            input("Press Enter to Continue")
            return
    print("Ticker not found")
    input("Press Enter to Continue")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol, end=" ")
    print("]")
    symbol = input("Which stock do you want to delete?: ")
    for stock in stock_list:
        if stock.symbol == symbol:
            stock_list.remove(stock)
            print(symbol, "Deleted")
            input("Press Enter to Continue")
            return
    print("Ticker not found")
    input("Press Enter to Continue")
def list_stocks(stock_list):
    clear_screen()
    print("Stock List ----")
    print(f"{'SYMBOL':<10}{'NAME':<20}{'SHARES'}")
    print("=" * 40)
    for stock in stock_list:
        print(f"{stock.symbol:<10}{stock.name:<20}{stock.shares}")
    input("\nPress Enter to Continue ***")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ----")
    print("Available stocks:", [s.symbol for s in stock_list])
    symbol = input("Which stock do you want to use?: ")
    for stock in stock_list:
        if stock.symbol == symbol:
            print("Ready to add data for:", symbol)
            print("Enter Data Separated by Commas - Do Not use Spaces")
            print("Enter a Blank Line to Quit")
            print("Enter Date,Price,Volume")
            print("Example: 5/07/26,99.75,11550")
            while True:
                row = input("Enter Date,Price,Volume: ")
                if row == "":
                    break
                parts = row.split(",")
                date = datetime.strptime(parts[0], "%m/%d/%y")
                price = float(parts[1])
                volume = int(parts[2])
                daily = DailyData(date, price, volume)
                stock.DataList.append(daily)
            return
    print("Ticker not found")
    input("Press Enter to Continue")
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_data:
        print(f"\nReport for:  {stock.symbol} {stock.name}")
        print(f"Shares:  {stock.shares}")
        if len(stock.DataList) == 0:
            print("*** No daily history.")
        else:
            print(f"\n{'Date':<10}{'Close Price':<20}{'Volume'}")
            print("=" * 40)
            for daily_data in stock.DataList:
                date_str = daily_data.date.strftime("%m/%d/%y")
                price_str = '${:0,.2f}'.format(daily_data.close)
                print(f"{date_str:<10}{price_str:<20}{daily_data.volume}")
    print("\n--- Report Complete ---")
    input("Press Enter to Continue")


# Display Chart
def display_chart(stock_list):
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol, end=" ")
    print("]")
    symbol = input("Which stock do you want to use?: ")
    display_stock_chart(stock_list, symbol)

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        while option not in ["1", "2", "3", "4", "0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")
        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data saved.")
            input("Press Enter to Continue")
        elif option == "2":
            stock_list.clear()
            stock_data.load_stock_data(stock_list)
            print("Data loaded.")
            input("Press Enter to Continue")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
        else:
            print("Returning to Main Menu")


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieving Stock Data from Yahoo! Finance ---")
    print("This will retrieve data from all stocks in your stock list.")
    date_from = input("Enter starting date: (MM/DD/YY): ")
    date_to = input("Enter ending date: (MM/DD/YY): ")
    try:
        record_count = stock_data.retrieve_stock_web(date_from, date_to, stock_list)
        print("Records Retrieved:", record_count)
    except:
        print("Could not retrieve data")
    input("Press Enter to Continue")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV file from Yahoo! Finance---")
    print("Which stock? Current list:")
    for stock in stock_list:
        print("  ", stock.symbol)
    symbol = input("Enter symbol: ")
    filename = input("Enter filename: ")
    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print("CSV File Imported")
    except:
        print("Check the filename and try again")
    input("Press Enter to Continue")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()