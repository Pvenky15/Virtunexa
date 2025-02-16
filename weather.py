import requests
import tkinter as tk
from tkinter import messagebox

API_KEY = "46e9f577e957f258798cf3a23e2597fb"
BASE_URL = "http://api.weatherstack.com/current"

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    url = f"{BASE_URL}?access_key={API_KEY}&query={city}"
    response = requests.get(url)
    data = response.json()

    if "current" in data:
        try:
            weather_info = f"""
            City: {data['location']['name']}
            Temperature: {data['current']['temperature']}°C
            Humidity: {data['current']['humidity']}%
            Wind Speed: {data['current']['wind_speed']} km/h
            Condition: {data['current']['weather_descriptions'][0]}
            """
            messagebox.showinfo("Weather Info", weather_info)
        except KeyError:
            messagebox.showerror("Error", "Unexpected API response format.")
    else:
        error_message = data.get("error", {}).get("info", "Unknown error occurred.")
        messagebox.showerror("Error", f"API Error: {error_message}")


root = tk.Tk()
root.title("Weather App")
root.geometry("300x200")

tk.Label(root, text="Enter City:").pack(pady=5)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=get_weather).pack(pady=10)

root.mainloop()
