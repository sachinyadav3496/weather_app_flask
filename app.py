import requests
from flask import Flask, render_template, request
import sqlite3 as sql 
import time

app = Flask(__name__)

key = "1a4c4f306c55a790989a33c6b9d37973"
@app.route('/', methods=['GET', 'POST'])
def index():
	cities=[]
	weather_data={}
	db = sql.connect("cities.db")
	cursor = db.cursor()	
	if request.method == 'POST':
		new_city = request.form.get('city')
		cursor.execute("select * from city") 
		cities = [ city[0] for city in cursor.fetchall() ]
		cities1=cities.copy()
		if new_city and new_city not in cities :
			
			cities.append(new_city)
		cities.remove(new_city)
		cities.append(new_city)
	
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
	weather_data = []
	print(cities)
	cities.reverse()
	for city in cities:
		try:

			r = requests.get(url.format(city,key)).json()

			weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        	}
			weather_data.append(weather)
		except:
			cities.remove(city)
			error='Incorrect city'
			return render_template('index.html',error=error)
	
	for city in cities:
		if city not in cities1:
			cursor.execute(f"insert into city values('{city}')")
			db.commit()
	db.close()
	return render_template('index.html', weather_data=weather_data)

if __name__ == "__main__" : 

	app.run("localhost",8088,debug=True)
