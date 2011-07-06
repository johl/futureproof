"""
views.py

URL routes and handlers

"""

from flask import render_template, flash, url_for, redirect, request
from models import QuestionModel

def home():
    return render_template('index.html')

def add_question():
    """Add a question to the database"""
    q = QuestionModel(question=request.form['entry'])
    q.save()
    return redirect(url_for('home'))


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

