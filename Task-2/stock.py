import requests
import tkinter as tk
from tkinter import messagebox
import datetime

API_KEY = "OLA30XAN6A3CIPBN"
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_price():
    symbol = entry.get().upper()
    if not symbol:
        messagebox.showerror("Error", "Please enter a stock ticker symbol.")
        return
    try:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if "Global Quote" not in data:
            messagebox.showerror("Error", f"No data found for {symbol}. Check the ticker symbol.")
            return
        
        quote = data["Global Quote"]
        stock_info = (
            f"Stock: {symbol}\n"
            f"Current Price: ${quote.get('05. price', 'N/A')}\n"
            f"Open: ${quote.get('02. open', 'N/A')}\n"
            f"High: ${quote.get('03. high', 'N/A')}\n"
            f"Low: ${quote.get('04. low', 'N/A')}\n"
            f"Previous Close: ${quote.get('08. previous close', 'N/A')}"
        )
        result.set(stock_info)
        log_operation(symbol, stock_info)
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

def log_operation(symbol, stock_info):
    with open("stock_price_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - {symbol}:\n{stock_info}\n\n")

app = tk.Tk()
app.title("Stock Price Viewer")

tk.Label(app, text="Enter Stock Ticker Symbol:").pack()
entry = tk.Entry(app)
entry.pack()

tk.Button(app, text="Get Stock Price", command=get_stock_price).pack()

result = tk.StringVar()
tk.Label(app, textvariable=result, justify=tk.LEFT).pack()

app.mainloop()