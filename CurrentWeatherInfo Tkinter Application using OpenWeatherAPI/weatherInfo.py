#### Tkinter Weather Information Application Using Open Weather API

import tkinter as tk
import bs4
import requests
from PIL import Image, ImageTk
import urllib.request
#import cv2

#Globals

Temperature = ""
cityName = ""
#Screen

root = tk.Tk()
root.minsize(800, 600)
root.config(bg='#222222')
root.title("Weather Information")

#Label Box

head = tk.Label(root, font=('Cursive', 25, 'bold'))
head.config(bg='#333333', fg='#fffeee', text='Enter the city name', width=30, relief=tk.RAISED)
head.pack(side=tk.TOP, pady=50)

#Entry Box

city = tk.Entry(root, font=('Cursive', 25, 'bold', 'italic'))
city.config(bg="#333333", fg="#fffeee", text="", width=30, relief=tk.RAISED)
city.pack(side=tk.TOP)

#ResultBox

result = tk.Label(root, font=('Cursive', 25, 'bold', 'italic'))
result.config(bg='#323232', fg='#fffeee', text=".............", width=30, relief=tk.RAISED)
result.pack(side=tk.TOP, pady=50)

#Canvas for icon

canvas = tk.Canvas(root)
canvas.config(bg="#aaaaaa", width=200, height=50, bd=0, relief=tk.RIDGE, highlightthickness=0)

#Exit

exit_button = tk.Button(root, font=('Cursive', 25, 'bold'))
exit_button.config(bg='#ff0000', fg='#000000', text="EXIT", width=20, height=1, command=root.quit)
exit_button.pack(side=tk.BOTTOM)






#Weather API Call
def show_weather(e):
    global Temperature, cityName
    degree_sign = u'\N{DEGREE SIGN}'
    key = "ad49a084c8af3f6e8b055da7750548f4"
    cityName = city.get()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={key}&units=metric"
    page = requests.get(url)
    #print(page.status_code)
    #print(page.content)
    data = dict(page.json())
    #print(data['weather'])
    Temperature = data['main']['temp']
    result.config(text=str(Temperature) + f" {degree_sign} C")
    icon = data['weather'][0]['icon']
    #print(icon)
    icon_url = f'http://openweathermap.org/img/wn/{icon}.png'
    img = Image.open(urllib.request.urlopen(icon_url))
    #img = Image.open('icon.ppm')
    img = img.resize((80, 80), Image.ANTIALIAS)
    #img.show()
    image = ImageTk.PhotoImage(img)
    canvas.create_image(100, 25, anchor=tk.CENTER, image=image)
    canvas.image = image
    canvas.pack(side=tk.TOP, pady=10)
    print("execution completed ...............")

city.bind('<Return>', show_weather)

root.mainloop()