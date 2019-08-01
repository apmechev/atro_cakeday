import os
import pdb

from flask import Flask
from flask import render_template 
from flask import flash
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.fields import DateField

from astro_cakeday.populate_cal import populate_ical

class MyForm(FlaskForm):
    name =  StringField('Your Name')
#    birthdate = DateField(id='birthday')
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

    # a simple page that says hello
    @app.route('/',  methods=['GET', 'POST'])
    def hello():
        form = MyForm()
        if form.validate_on_submit():
            populate_ical(person_name=form.name.data,  birthday=form.date.data)
            return  
        return render_template('birthday.html', form=form)
  
    return app
