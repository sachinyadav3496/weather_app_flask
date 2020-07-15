import requests
from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

key = "57af8679ea543de62eeaa80d2ffac36f"

db = sql.connect("cities.db")
cursor = db.cursor()
cursor.execute('delete from city')
db.commit()
cursor.close()
db.close()

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
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
	weather_data = []
	for city in cities:
		r = requests.get(url.format(city,key))
		print(r.status_code)
		print(r.headers['Content-type'])
		print(r.json())
		if r.status_code == 200 and 'json' in r.headers['Content-type']:
			r = r.json()
			weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            					}
		else:
			weather = {
            'city' : f'{city }NA with response {r.status_code}',
            'temperature' : 'not available',
            'description' : 'not available',
            'icon' : '01n',
            }
		weather_data.append(weather)

	return render_template('index.html', weather_data=weather_data)



if __name__ == "__main__" :

	app.run("localhost",80,debug=True)
