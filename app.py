import requests
from flask import Flask, render_template, request
import sqlite3 as sql 

app = Flask(__name__)

key = "1a4c4f306c55a790989a33c6b9d37973"
@app.route('/', methods=['GET', 'POST'])
def index():
	db = sql.connect("cities.db")
	cursor = db.cursor()	
	if request.method == 'POST':
		new_city = request.form.get('city')
		cursor.execute("select * from city") 
		cities = [ city[0] for city in cursor.fetchall() ]
		if new_city and new_city not in cities :
			cursor.execute(f"insert into city values('{new_city}')")
			db.commit()
	cursor.execute("select * from city")
	cities = [ city[0] for city in cursor.fetchall() ]
	cursor.close()
	db.close()
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
	weather_data = []
	for city in cities:
		r = requests.get(url.format(city,key)).json()
		weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
		weather_data.append(weather)
	return render_template('index.html', weather_data=weather_data)
	
	
	
if __name__ == "__main__" : 

	app.run("localhost",8088,debug=True)