"""
views.py

URL routes and handlers

"""


from google.appengine.api import users

from flask import render_template, flash, url_for, redirect

from models import QuestionModel
#from forms import ExampleForm


def home():
    return render_template('index.html')

def add_question(request):
    """Add a question to the database"""
    flash('New entry was successfully posted')
    return redirect(url_for('home'))


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

