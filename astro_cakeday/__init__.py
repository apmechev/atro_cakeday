import os

from flask import Flask
from flask import render_template 
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms.fields import DateField

class MyForm(Form):
    date = DateField(id='datepick')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='sdafsadfsa',
    )
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
    @app.route('/')
    def hello():
        form = MyForm()
        return render_template('birthday.html', form=form)

    return app
