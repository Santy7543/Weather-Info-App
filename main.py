from tkinter import Tk, Label, Button, StringVar, Entry, ttk
import tkinter.messagebox
import requests
import textwrap


def get_data(event=None):
    # print("Fetching Data...")
    weatherSumBox.config(text=" ")

    loadingLabel = Label(
        root, text="Loading... ", font=(
            "Arial", 13, "italic"), bg="#c3e090")
    loadingLabel.place(x=350, y=60)
    loadingLabel.update()

    selected_interval = timeInt.get()

    zip = zip_code.get()
    if zip.isdigit() is False or len(zip) != 5:
        loadingLabel.config(text="Invalid    ")
        loadingLabel.update()
        tkinter.messagebox.showinfo(
            "ERROR", "Please enter valid U.S. ZIP code.")
        # print("invalid ZIP code")
        return

    geoAPI_url = "http://api.openweathermap.org/geo/1.0/zip?zip=" + \
        zip + ",US&appid=API_KEY_HERE"  # <---Enter API key
    zipData = requests.get(geoAPI_url)

    if zipData.status_code != 200:
        loadingLabel.config(text="Invalid    ")
        loadingLabel.update()
        tkinter.messagebox.showinfo(
            "ERROR", "Please enter valid U.S. ZIP code.")
        # print("invalid ZIP code")

    zipData = zipData.json()
    lat = str(zipData["lat"])
    lon = str(zipData["lon"])

    weatherAPI_url = (
        "https://api.openweathermap.org/data/3.0/onecall?lat=" +
        lat + "&lon=" + lon +
        "&exclude=minutely,hourly,daily&units=imperial" +
        "&appid=API_KEY_HERE")  # <---Enter API key

    weatherData = requests.get(weatherAPI_url).json()
    # print(weatherData)
    loadingLabel.config(text="Done!  ")
    weatherDataLabel.config(
        text=weatherData["current"]["weather"][0]["description"])
    windDataLabel.config(
        text=str(
            weatherData["current"]["wind_speed"]) +
        "mph")
    tempDataLabel.config(text=str(weatherData["current"]["temp"]) + "°F")
    humidDataLabel.config(text=str(weatherData["current"]["humidity"]) + "%")
    hPaDataLabel.config(text=str(weatherData["current"]["pressure"]) + "hPa")

    summaryAPI_url = (
        "https://api.openweathermap.org/data/3.0/onecall/overview?lat=" +
        lat + "&lon=" + lon +
        "&units=imperial&appid=API_KEY_HERE")  # <---Enter API key

    summaryData = requests.get(summaryAPI_url).json()
    sumText = textwrap.fill(summaryData["weather_overview"], width=40)
#    print(sumText)
    weatherSumLabel = Label(
        root, text="Weather Overview Description", font=(
            "Trebuchet MS", 20, "bold"), bg="#c3e090")
    weatherSumLabel.place(x=36, y=370)
    root.geometry("450x850")
    weatherSumBox.config(text=sumText)

    if selected_interval == "once" or not selected_interval:
        return
    elif selected_interval == "10 sec":
        interval = 10 * 1000  # 10 seconds in milliseconds
    elif selected_interval == "5 min":
        interval = 5 * 60 * 1000  # 5 minutes
    elif selected_interval == "15 min":
        interval = 15 * 60 * 1000  # 15 minutes
    elif selected_interval == "30 min":
        interval = 30 * 60 * 1000  # 30 minutes
    elif selected_interval == "1 hour":
        interval = 60 * 60 * 1000  # 1 hour
    root.after(interval, get_data)


root = Tk()
root.geometry("450x450")
root.title("Weather Tracker")
root.config(bg="#c3e090")

zip_code = StringVar()
zip_entry = Entry(root, textvariable=zip_code, font=("Arial", 13), width=20)
zip_entry.place(x=120, y=60, height=30)

intervalLabel = Label(root, text="Interval", font=("Arial", 13), bg="#c3e090")
intervalLabel.place(x=285, y=109)
timeInt = StringVar()
time_intervals = ["once", "10 sec", "5 min", "15 min", "30 min", "1 hour"]
dropDown = ttk.Combobox(
    root,
    values=time_intervals,
    textvariable=timeInt,
    font=(
        'Arial',
        7),
    state="readonly")
dropDown.place(x=350, y=105, height=30, width=50)

infoLabel = Label(
    root,
    text="Enter U.S. ZIP code",
    font=(
        "Trebuchet MS",
        20,
        "bold"),
    bg="#c3e090")
infoLabel.place(x=90, y=20)
weatherLabel = Label(
    root,
    text="Weather",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090")
weatherLabel.place(x=80, y=160)
windLabel = Label(root, text="Wind", font=("Trebuchet MS", 15), bg="#c3e090")
windLabel.place(x=80, y=240)
tempLabel = Label(
    root,
    text="Temperature",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090")
tempLabel.place(x=80, y=200)
humidLabel = Label(
    root,
    text="Humidity",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090")
humidLabel.place(x=80, y=280)
hPaLabel = Label(
    root,
    text="Pressure",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090")
hPaLabel.place(x=80, y=320)

weatherDataLabel = Label(
    root,
    text=" ",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090",
    fg="#008B00")
weatherDataLabel.place(x=265, y=160)
windDataLabel = Label(
    root,
    text=" ",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090",
    fg="#008B00")
windDataLabel.place(x=265, y=240)
tempDataLabel = Label(
    root,
    text=" ",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090",
    fg="#008B00")
tempDataLabel.place(x=265, y=200)
humidDataLabel = Label(
    root,
    text=" ",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090",
    fg="#008B00")
humidDataLabel.place(x=265, y=280)
hPaDataLabel = Label(
    root,
    text=" ",
    font=(
        "Trebuchet MS",
        15),
    bg="#c3e090",
    fg="#008B00")
hPaDataLabel.place(x=265, y=320)


btn = Button(
    root,
    text="Check Weather",
    font=(
        "Arial",
        13),
    bg="#E6E6FA",
    bd=5,
    command=get_data,
    width=15)
btn.place(x=80, y=100)

weatherSumBox = Label(root, text=" ", font=("Trebuchet MS", 15), bg="#c3e090")
weatherSumBox.place(x=36, y=425)

root.bind("<Return>", get_data)


root.mainloop()
