from os import path
import tkinter as tk
from tkinter import font
from tkinter.messagebox import *
import requests, base64
from PIL import Image, ImageTk

# main
# basic info
api_key = "14a824e9660c3c56278deb50b0f7a049"
base_url = "http://api.openweathermap.org/data/2.5/weather?"


# GUI
def getIcon(icon_id):
    url = "http://api.openweathermap.org/img/wn/icon.png".format(icon=icon_id)
    response = requests.get(url, stream=True)
    return base64.encodebytes(response.raw.read())


def findWeather():
    city_name = city.get()
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidty = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        temperature = str((current_temperature - 273.15) * (0.5))
        icon = getIcon(z[0]["icon"])
        showWeather([
            city_name,
            temperature,
            current_humidty,
            current_pressure,
            icon,
            z[0]["description"],
        ])

    else:
        showerror("Error", "City Not Valid!\nPlease Check!")
        city.delete(0, tk.END)


def showWeather(data1):
    global x
    newScreen = tk.Toplevel()
    newScreen.title("Weather Result")
    newScreen.geometry("390x675")
    newScreen.resizable(0, 0)
    bg_picture = ImageTk.PhotoImage(Image.open("bg.jpg"))
    bg = tk.Label(newScreen, image=bg_picture)
    bg.pack()
    # icon_image = tk.PhotoImage(data=data1[4])
    # icon_label = tk.Label(newScreen,image=icon_image)
    # icon_label.place(x=0,y=15)

    desc = tk.Label(newScreen, text=data1[5], font=("Times", 15, "bold"))
    desc.place(x=80, y=80)

    location = tk.Label(newScreen,
                        text=f"Location : {data1[0]}",
                        font=("Times", 13))
    location.place(x=80, y=150)

    temperature = tk.Label(newScreen,
                           text=f"Temperature : {data1[1]}°C",
                           font=("Times", 13))
    temperature.place(x=80, y=200)

    current_humidity = tk.Label(newScreen,
                                text=f"Humidity : {data1[2]}%",
                                font=("Times", 13))
    current_humidity.place(x=80, y=250)

    current_pressure = tk.Label(newScreen,
                                text=f"Pressure : {data1[3]}",
                                font=("Times", 13))
    current_pressure.place(x=80, y=300)

    close_button = tk.Button(
        newScreen,
        text="Close",
        command=lambda: [city.delete(0, tk.END),
                         newScreen.destroy()],
        font=("Times", 15, "bold"),
        bg="#121212",
        fg="#fafef8",
    )
    close_button.place(x=150, y=400)

    newScreen.mainloop()


root = tk.Tk()
root.title("Weather App")
root.geometry("390x650")
root.resizable(0, 0)
bg_picture = ImageTk.PhotoImage(Image.open("bg.gif"))
bg = tk.Label(root, image=bg_picture)
bg.pack()
tit_le = tk.Label(
    root,
    text="Enter City Below",
    font=("Times", 20, "bold"),
    bg="#1f252f",
    fg="#fafef8",
)
tit_le.place(x=110, y=300)
city = tk.Entry(root, font=("Times", 15))
city.place(x=110, y=350)
city.focus()
cta_button = tk.Button(root, text="Find Weather", command=findWeather)
cta_button.place(x=165, y=400)
root.mainloop()
