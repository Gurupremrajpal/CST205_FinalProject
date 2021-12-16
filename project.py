'''
Course - CST 205
Title - Multimedia Design & Programming
Abstract - Survey and Weather application 
Authors - Guruprem, Prajwal, Shyam
Date- 11 December 2021

Work Done-
Guruprem- login.html, index.html, dataase.html, front.html, project.py
Prajwal- weather.html, project.py
Shyam- jobindex.html

Important code blocks - 
Important code blocks are class user, store_details

Sources - 
https://flask-login.readthedocs.io/en/latest/
https://openweathermap.org

GitHub- 
https://github.com/Gurupremrajpal/CST205_FinalProject

'''



from flask import Flask, render_template, redirect, request, session, url_for, g
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
import smtplib
from pprint import pprint
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from PIL import Image

app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'csumb-otter'
app.secret_key = 'csumb-otter'





class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'



users = []
users.append(User(id=1, username='user', password='P@ssword'))



@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']]
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('frontpg'))
        return redirect(url_for('login'))

    return render_template('login.html')




class plist(FlaskForm):
    first_name = StringField(
        'First Name:',
        validators =[DataRequired()])
    last_name = StringField(
        'Last Name:',
        validators=[DataRequired()])
    email_id = StringField(
        'Email:',
        validators=[DataRequired()])
    Pno = StringField(
        'Phone Number:',
        validators=[DataRequired()])
    zipNo = StringField(
        'Zip Code:',
        validators=[DataRequired()]
    )
    city = StringField(
        'City:',
        validators=[DataRequired()]
    )
    state = StringField(
        'State:',
        validators=[DataRequired()]
    )
    county = StringField(
        'County:',
        validators=[DataRequired()]
    )
    
database = []


def store_detail(my_firstname, my_lastname, my_email, my_phone, my_zip, my_city, my_state, my_county):
    database.append(dict(
        fname= my_firstname,
        lname= my_lastname,
        email= my_email,
        phonenumber= my_phone,
        zipnumber= my_zip,
        cityy= my_city,
        statee= my_state,
        countyy = my_county,
        date = datetime.today()
    ))


@app.route('/survey', methods=('GET', 'POST'))
def survey():
    form = plist()
    if not g.user:
        return redirect(url_for('/'))
    
    if form.validate_on_submit():
        store_detail(form.first_name.data, form.last_name.data, form.email_id.data,
                     form.Pno.data, form.zipNo.data, form.city.data, form.state.data, form.county.data)
        print(plist)
        return redirect('/end')
    
    return render_template('index.html', form=form)


@app.route('/front', methods =('GET', 'POST'))
def frontpg():
    return render_template('front.html')


@app.route('/weatherpg', methods=('GET', 'POST'))
def weatherpg():
    Weather_data = []
    try:
        print("weatherpg")
        if request.method == "POST":
            print("POST REQUEST")
            _City = request.form['city']    # Getting values from form
            _Country = request.form['country']      # Getting values from form
            print("*****************")
            print(_City)
            print(_Country)
            # calling the Weather_get Function to get Weather deatials
            Weather_data = Weather_get(_City, _Country)
            print("Weather_data : ", Weather_data)
    except:
        Weather_data = []
        print("Exception : ")
        # Render the HTML Page and parsing the Weather Data
        return render_template("weather.html", Weather_data=Weather_data, data=1, message='Your Entered Wrong City Name')

    return render_template("weather.html", Weather_data=Weather_data, data=0, message='')


def Weather_get(_City, _Country):
    Weather_data = []       # Array for store Weather data
    url = 'http://api.openweathermap.org/data/2.5/weather?units=imperial&appid=57f9401ec88509d93821bc0cfeabd3c2&q=' + \
        str(_City)     # Creat API url based by the enterd data
    # Requseting Weather detials frome the API
    weather_data = requests.get(url).json()
    # print(weather_data['main']['temp'])
    # print(weather_data['main']['humidity'])
    # print(weather_data['wind']['speed'])
    # Filltering the response data and add to the list
    print("*****************")
    print("Wether Data 1")
    Weather_data = Weather_data + [str(weather_data['main']['temp']), str(
        weather_data['main']['humidity']), str(weather_data['wind']['speed'])]

    return Weather_data

@app.route('/end', methods=('GET', 'POST'))
def end():
    return render_template('end.html')

@app.route('/data_base')
def db():
    return render_template('database.html', database=database)




