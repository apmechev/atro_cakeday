import os
import pdb

from flask import Flask
from flask import request
from flask import render_template 
from flask import send_from_directory 
from flask import flash
from flask import url_for 
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms import SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired

from astro_cakeday.populate_cal import populate_ical
from astro_cakeday.planets import PLANET_DB

class MyForm(FlaskForm):
    name = StringField('Your Name')
    birthyear = IntegerField('Year', default=1999)
    birthmonth = IntegerField('Month', default=1)
    birthday = IntegerField('Day', default=1)
    mercury_stagger = IntegerField('Skip Mercury Birthdays by', default=5)
    venus_stagger = IntegerField('Skip Venus Birthays by', default=2)
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
            flash('user {}, birthday={}/{}/{}'.format(
            form.name.data, form.birthyear.data, form.birthmonth.data, form.birthday.data))
            birthdate = "{}-{}-{}".format(form.birthyear.data, form.birthmonth.data, form.birthday.data)
            PLANET_DB['Mercury'] = int(form.mercury_stagger.data)
            PLANET_DB['Venus'] = int(form.venus_stagger.data)
            icalfile = populate_ical(person_name=form.name.data,  birthday=birthdate,
                                     PLANET_DB=PLANET_DB)
#            return send_from_directory('uploads', icalfile.split('uploads/')[-1]) 
            return render_template('result.html', filename=icalfile)
 

        return render_template('birthday.html', form=form)

    return app
