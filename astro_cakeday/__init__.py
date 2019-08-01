import os
import pdb

from flask import Flask
from flask import request
from flask import render_template 
from flask import flash
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired

from astro_cakeday.populate_cal import populate_ical


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    birthdate = DateField(id='birthday')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



class MyForm(FlaskForm):
    name =  StringField('Your Name')
    birthdate = DateField(id='.dp')
    submit = SubmitField('Give me my birthday:)')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='sdafsadfsa',
    )
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    datepicker(app)
    Bootstrap(app)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/',  methods=['GET', 'POST'])
    def hello():
        form = MyForm()
        if request.method == 'POST':
            flash('user {}, birthday={}'.format(
            form.name.data, form.birthdate.data))
#            populate_ical(person_name=form.name.data,  birthday=form.date.data)
            return  render_template('test.html', form=form)

        return render_template('birthday.html', form=form)

    @app.route('/login')
    def login():
        form = LoginForm()
        return render_template('login.html', title='Sign In', form=form)

    return app
