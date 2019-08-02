import os
import datetime

from flask import Flask
from flask import request
from flask import render_template 
from flask import send_from_directory 
from flask import flash
from flask.logging import default_handler

from flask import url_for 
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField
from wtforms import SubmitField
from wtforms.validators import DataRequired

from astro_cakeday.populate_cal import populate_ical
from astro_cakeday.planets import PLANET_DB

##TODO: give next few birthdays

class MyForm(FlaskForm):
    name = StringField('Your Name')
    birthyear = IntegerField('Year', default=1999)
    birthmonth = IntegerField('Month', default=1)
    birthday = IntegerField('Day', default=1)
    mercury_stagger = IntegerField('Skip Mercury Birthdays by', default=2)
    venus_stagger = IntegerField('Skip Venus Birthdays by', default=1)

#    birthdate = DateField("Choose a date", id='.dp')

    cal_start = IntegerField('Start Year', default=1999)
    cal_end = IntegerField('End Year', default=2100)
    submit = SubmitField('Give me my birthday:)')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='sdafsadfsa',
    )
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    Bootstrap(app)
    
    datepicker.picker(dp, dateFormat='yyyy-mm-dd', id='.dp', minDate='1900-01-01', btnsId='dpbtn')

    app.logger.addHandler(default_handler)
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
        if request.user_agent:
            user_agent = request.user_agent.string
            platform = request.user_agent.platform
            browser = request.user_agent.browser
            language = request.user_agent.language
        app.logger.info("visit from ip:{}, pltf:{}, brws:{}, lng:{}".format(request.remote_addr,
                    platform, browser, language))
        app.logger.info("full_user_agent: {}".format(user_agent))
        app.logger.info("Referrer: {}".format(request.referrer))
        form = MyForm()
        if request.method == 'POST':
            day = form.birthday.data
            month = form.birthmonth.data
            year = form.birthyear.data
            start_year = form.cal_start.data
            end_year = form.cal_end.data
            birthdate = "{}-{}-{}".format(year, month, day)
            cal_start = '{}-01-01'.format(start_year)
            cal_end = '{}-01-01'.format(end_year)
            try:
                datetime.datetime(year=year, month=month, day=day)
            except Exception as e:
                return "ERROR: {}".format(str(e))

            PLANET_DB['Mercury'] = int(form.mercury_stagger.data)
            PLANET_DB['Venus'] = int(form.venus_stagger.data)

            icalfile = populate_ical(person_name=form.name.data,  birthday=birthdate,
                                     PLANET_DB=PLANET_DB, cal_start=cal_start,
                                     cal_end=cal_end)
            return render_template('result.html', filename=icalfile)
 

        return render_template('birthday.html', form=form)

    return app
