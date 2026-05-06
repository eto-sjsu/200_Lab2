#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

def sortStocks(stock_list):
    if len(stock_list) <= 1:
        return
    stack = []
    stack.append(0)
    stack.append(len(stock_list) - 1)

    while len(stack) > 0:
        high = stack.pop()
        low = stack.pop()

        if low < high:
            pivot = stock_list[high].symbol
            i = low - 1
            j = low
            while j < high:
                if stock_list[j].symbol <= pivot:
                    i = i + 1
                    temp = stock_list[i]
                    stock_list[i] = stock_list[j]
                    stock_list[j] = temp
                j = j + 1
            temp = stock_list[i + 1]
            stock_list[i + 1] = stock_list[high]
            stock_list[high] = temp
            pivot_index = i + 1
            stack.append(low)
            stack.append(pivot_index - 1)
            stack.append(pivot_index + 1)
            stack.append(high)


def sortDailyData(stock_list):
    if len(stock_list) == 0:
        return

    if hasattr(stock_list[0], 'DataList'):
        data_lists = [stock.DataList for stock in stock_list]
    else:
        data_lists = [stock_list]

    for data_list in data_lists:
        if len(data_list) <= 1:
            continue

        stack = []
        stack.append(0)
        stack.append(len(data_list) - 1)

        while len(stack) > 0:
            high = stack.pop()
            low = stack.pop()

            if low < high:
                pivot = data_list[high].date
                i = low - 1
                j = low
                while j < high:
                    if data_list[j].date <= pivot:
                        i = i + 1
                        temp = data_list[i]
                        data_list[i] = data_list[j]
                        data_list[j] = temp
                    j = j + 1
                temp = data_list[i + 1]
                data_list[i + 1] = data_list[high]
                data_list[high] = temp
                pivot_index = i + 1

                stack.append(low)
                stack.append(pivot_index - 1)
                stack.append(pivot_index + 1)
                stack.append(high)

def display_stock_chart(stock_list, symbol):
    for stock in stock_list:
        if stock.symbol == symbol:
            if len(stock.DataList) == 0:
                print("No daily data to chart for", symbol)
                return
            dates = [d.date for d in stock.DataList]
            prices = [d.close for d in stock.DataList]

            plt.figure()
            plt.plot(dates, prices)
            plt.title(stock.name)
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.tight_layout()
            plt.show()
            return
    print("Stock not found:", symbol)