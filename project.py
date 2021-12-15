'''
Course - CST 205
Title - Multimedia Design & Programming
Abstract - Survey and Weather application 
Authors - Guruprem, Prajwal, Shyam
Date- 11 December 2021

Work Done-
Guruprem- login.html, index.html, dataase.html, front.html, project.py
Prajwal- weather.html, project.py
Shyam- 

Important code blocks - 

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


@app.route('/weather', methods=('GET', 'POST'))
def weatherpg():
    return render_template('weather.html')

@app.route('/end', methods=('GET', 'POST'))
def end():
    return render_template('end.html')

@app.route('/data_base')
def db():
    return render_template('database.html', database=database)




