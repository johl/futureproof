"""
views.py

URL routes and handlers

"""

from flask import render_template, url_for, redirect, request
from models import Question

def home():
    questions = Question.gql( "WHERE aproved = yes" ).get()
    print questions
    return render_template('index.html')

def add_question():
    """Add a question to the database"""
    if ('entry' in request.form):
        q = Question(question=request.form['entry'], aproved="no")
        q.save()
    return redirect(url_for('home'))


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

