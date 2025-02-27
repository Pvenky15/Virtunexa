import tkinter as tk
from tkinter import messagebox
import requests
import sqlite3
import time
import threading


API_KEY = "3fd210d3668ee32641869bee54fe65a8"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        return f"Weather: {weather}, Temperature: {temp}°C"
    else:
        return "City not found!"


def setup_db():
    conn = sqlite3.connect("assistant_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT,
            response TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_to_db(command, response):
    conn = sqlite3.connect("assistant_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (command, response, timestamp) VALUES (?, ?, ?)" ,
                   (command, response, time.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def set_reminder(reminder_text, delay):
    time.sleep(delay)
    messagebox.showinfo("Reminder", reminder_text)


def start_reminder():
    reminder_text = reminder_entry.get().strip()
    delay_text = delay_entry.get().strip()
    
    if not delay_text.isdigit():
        messagebox.showerror("Error", "Please enter a valid number for delay.")
        return
    
    delay = int(delay_text)
    threading.Thread(target=set_reminder, args=(reminder_text, delay), daemon=True).start()
    messagebox.showinfo("Reminder Set", "Reminder has been set!")

def perform_calculation():
    try:
        expression = calc_entry.get()
        result = eval(expression)
        calc_result_label.config(text=f"Result: {result}")
        save_to_db(expression, str(result))
    except Exception:
        calc_result_label.config(text="Error")
        messagebox.showerror("Error", "Invalid calculation!")


def get_weather_info():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return
    
    weather_info = get_weather(city)
    weather_label.config(text=weather_info)
    save_to_db(city, weather_info)


root = tk.Tk()
root.title("Virtual Assistant")
root.geometry("400x500")


tk.Label(root, text="Weather Info", font=("Arial", 12, "bold")).pack(pady=5)
city_entry = tk.Entry(root)
city_entry.pack()
tk.Button(root, text="Get Weather", command=get_weather_info).pack()
weather_label = tk.Label(root, text="", font=("Arial", 10))
weather_label.pack()


tk.Label(root, text="Calculator", font=("Arial", 12, "bold")).pack(pady=5)
calc_entry = tk.Entry(root)
calc_entry.pack()
tk.Button(root, text="Calculate", command=perform_calculation).pack()
calc_result_label = tk.Label(root, text="", font=("Arial", 10))
calc_result_label.pack()


tk.Label(root, text="Set Reminder", font=("Arial", 12, "bold")).pack(pady=5)
reminder_entry = tk.Entry(root, width=30)
reminder_entry.pack()
delay_entry = tk.Entry(root, width=10)
delay_entry.pack()
tk.Button(root, text="Set Reminder", command=start_reminder).pack()

setup_db()


root.mainloop()
