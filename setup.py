from flask import Flask, render_template, redirect, url_for, flash, session 
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.fields import StringField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os
import smtplib
import imghdr
from email.message import EmailMessage
import sqlite3
import time
import datetime
import random
import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
style.use('fivethirtyeight')

###########################################################################################################

# create an instance of the Flask class
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

###########################################################################################################

# DATA BASE USUARIO
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)


#CARGAR DATOS DE USUARIO
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#LOGIN FORM
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

#REGISTER FORM
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
#EMAIL FORM
class PostForm(FlaskForm):
    title = StringField('Email', validators=[Length(max=50), DataRequired(), Email(message='Invalid email')])
    body = TextAreaField('Mensaje', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Post')


''' def SendWelcome():
                 conn = sqlite3.connect('database.db')
                 c = conn.cursor()
                 emails = c.execute("SELECT email FROM user;")
                 contacts = c.fetchall()
                 EMAIL_ADDRESS = os.environ.get('GJ_EMAIL_USER')
                 EMAIL_PASSWORD = os.environ.get('GJ_EMAIL_PASS')
                 for contact in contacts:
                     msg = EmailMessage()
                     msg['Subject'] = 'de JINSU - MI 1RA PAGINA WEB "CORONAVIRUS"'
                     msg['From'] = EMAIL_ADDRESS
                     msg['To'] = contact
                     msg.set_content('Bienvenido a la WEB de CoronaVirus. Te estaremos informando de toda la informacion relevante sobre el COVID-19 al rededor del mundo.')
         
                     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                         smtp.send_message(msg)    SendWelcome()'''
###########################################################################################################

submit = SubmitField()

@app.route('/main/',methods=['GET', 'POST'])
@login_required
def hello():
    form = PostForm()
    posts = Post.query.order_by(Post.id.desc()).all()
   
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, body=form.body.data)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('hello'), flash('Tu comentario ha sido publicado', "alert alert-success"))
    return render_template("index.html", form=form, posts=posts)

###########################################################################################################
#SIGNUP
@app.route("/", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'), flash('Se ha creado un nuevo usuario!',"alert alert-success")) 

    return render_template('signup.html', form=form)
# LOGIN 
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)

                return redirect(url_for('hello'), flash('Ha ingresado exitosamente!', "alert alert-success"))

            return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

###########################################################################################################
# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

###########################################################################################################
@app.route('/datos/', methods=['GET', 'POST'])
def datos():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT location, total_deaths FROM covdat WHERE date = "2020-05-07" ORDER BY cast(total_deaths as int) DESC')
    data = c.fetchall()
    return render_template('datos.html', data=data)

###########################################################################################################

if __name__=="__main__":
 app.run(debug=True)
