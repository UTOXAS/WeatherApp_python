import ctypes
import os
import sys
import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime, timedelta

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "utoxas.calculator_python"
)


API_KEY = "775e151451f1cda08020afaa7b34e227"

CURRENT_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

root = tk.Tk()
root.title("Weather App")
root.geometry("400x600")
root.resizable(False, False)


def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    try:
        current_params = {"q": city, "appid": API_KEY, "units": "metric"}
        current_response = requests.get(CURRENT_WEATHER_URL, params=current_params)
        current_data = current_response.json()

        if current_data["cod"] != 200:
            messagebox.showerror("Error", f"City not found: {current_data['message']}")
            return

        temp = current_data["main"]["temp"]
        humidity = current_data["main"]["humidity"]
        city_name = current_data["name"]

        current_label.config(text=f"{city_name}\n{temp}°C\nHumidity: {humidity}%")

        forecast_params = {"q": city, "appid": API_KEY, "units": "metric"}
        forecast_response = requests.get(FORECAST_URL, params=forecast_params)
        forecast_data = forecast_response.json()

        for widget in forecast_frame.winfo_children():
            widget.destroy()

        daily_forecasts = {}
        for item in forecast_data["list"]:
            date = datetime.fromtimestamp(item["dt"]).date()
            if date not in daily_forecasts and len(daily_forecasts) < 5:
                daily_forecasts[date] = item["main"]["temp"]

        for i, (date, temp) in enumerate(daily_forecasts.items()):
            day_label = tk.Label(
                forecast_frame,
                text=f"{date.strftime('%a, %d %b')}: {temp}°C",
                font=("Arial", 12),
                bg="#ECEFF1",
                pady=5,
            )
            day_label.pack()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")


def set_app_icon(icon_path):
    """Sets the application icon for the window and taskbar."""
    try:
        # self.root.iconbitmap(icon_path)
        icon = tk.PhotoImage(file=resource_path(icon_path))
        root.iconphoto(True, icon)

    except tk.TclError:
        print(
            f"Error: Could not set icon from {icon_path}. Check file path and format."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


set_app_icon("icon.png")

title_label = tk.Label(
    root, text="Weather App", font=("Arial", 20, "bold"), bg="#ECEFF1", fg="#37474F"
)
title_label.pack(pady=20)

city_frame = tk.Frame(root, bg="#ECEFF1")
city_frame.pack(pady=10)
tk.Label(city_frame, text="Enter City:", font=("Arial", 12), bg="#ECEFF1").pack(
    side=tk.LEFT, padx=5
)
city_entry = tk.Entry(city_frame, font=("Arial", 12), width=20)
city_entry.pack(side=tk.LEFT)

get_button = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 12),
    bg="#90A4AE",
    fg="white",
    command=get_weather,
)
get_button.pack(pady=10)

current_label = tk.Label(
    root,
    text="Enter a city to see weather",
    font=("Arial", 18),
    bg="#ECEFF1",
    fg="#455A64",
    justify="center",
)
current_label.pack(pady=20)

forecast_frame = tk.Frame(root, bg="#ECEFF1")
forecast_frame.pack(pady=20)

root.mainloop()
