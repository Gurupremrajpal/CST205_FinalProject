from flask import Flask, render_template, redirect, request, session, url_for, g
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
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
users.append(User(id=1, username='Anthony', password='password'))
users.append(User(id=2, username='Becca', password='secret'))
users.append(User(id=3, username='Guruprem', password='Rajpal'))



@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
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
            return redirect(url_for('survey'))

        return redirect(url_for('/'))

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
    
database = []


def store_detail(my_firstname, my_lastname, my_email, my_phone, my_zip):
    database.append(dict(
        fname= my_firstname,
        lname= my_lastname,
        email= my_email,
        phonenumber = my_phone,
        zipnumber =my_zip,
        date = datetime.today()
    ))


@app.route('/survey', methods=('GET', 'POST'))
def survey():
    form = plist()
    if not g.user:
        return redirect(url_for('/'))
    
    if form.validate_on_submit():
        store_detail(form.first_name.data, form.last_name.data, form.email_id.data, form.Pno.data, form.zipNo.data)
        print(plist)
        return redirect('/data_base')
    return render_template('ind.html', form=form)



@app.route('/data_base')
def db():
    return render_template('database.html', database=database)




