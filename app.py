import requests
from flask import Flask, render_template, request
import sqlite3 as sql 
from datetime import datetime

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
		print(new_city)
		cursor.execute("select * from city") 
		cities = [ city[0] for city in cursor.fetchall() ]
		cities1=cities.copy()
		if new_city and new_city not in cities :
			
			cities.append(new_city)
		try:
			cities.remove(new_city)
			cities.append(new_city)
		except:
			pass
	
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
			try:
				cities.remove(city)
			except:
				pass
			error='Incorrect city'
			return render_template('index.html',error=error)
	
	for city in cities:
		if city not in cities1:
			cursor.execute(f"insert into city values('{city}')")
			db.commit()
	db.close()
	return render_template('index.html', weather_data=weather_data)


@app.route('/details/<weather_city>', methods=['GET', 'POST'])
def details(weather_city):
	city=weather_city
	#print(city)
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
	url1='http://api.openweathermap.org/data/2.5/forecast?id={}&appid={}'
	r = requests.get(url.format(city,key)).json()

	ide=r['id']
	r1 = requests.get(url1.format(ide,key)).json()
	sr=r['sys']['sunrise']
	sr=datetime.fromtimestamp(sr)
	sr=str(sr)
	sr=sr.split(' ')
	st=r['sys']['sunset']
	st=datetime.fromtimestamp(st)
	st=str(st)
	st=st.split(' ')
	#print(r)
	list1=[]
	list2=[]
	list3=[]
	list4=[]
	list5=[]
	list6=[]
	list7=[]
	list8=[]
	for i in r1['list']:
		list1.append(i['weather'][0]['icon'])
		list5.append(i['main']['pressure'])
		list6.append(i['main']['humidity'])
		list7.append(i['clouds']['all'])
		list4.append(i['wind']['speed'])
		x=i['dt_txt'].split(' ')
		list2.append(x[0])
		list3.append(x[1])
		list8.append(round(int(i['main']['temp'])-273.15,2))
		t=round(((int(r['main']['temp'])-32)*(5/9)),2)
	weather = {
            'city' : city,
            
            'temperature' : t,
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
           	'sunrise' : sr[1],
            'sunset' : st[1],
            'humidity' : str(r['main']['humidity'])+'%',
            'geo_coords' : r['coord'],
            'pressure' : str(r['main']['pressure'])+'hpa',
            'wind_speed' : r['wind']['speed']
        	}
	
    #data=zip(list3,list1,list8,list5,list6,list4,list7)  	

	return render_template('details.html',weather=weather,list1=list1,list2=list2,list3=list3,list4=list4,list5=list5,list6=list6,list7=list7,list8=list8)


if __name__ == "__main__" : 

	app.run("localhost",8088,debug=True)
