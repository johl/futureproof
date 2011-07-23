"""
views.py

URL routes and handlers

"""

from flask import render_template, url_for, redirect, request
from models import Question
from types import *

def home():
    questions = Question.gql( "WHERE aproved = 'yes'" ).fetch(limit=100)
    if (not type(questions) == NoneType):
        return render_template('index.html', questions=questions)
    else:
        return render_template('index.html')

def add_question():
    """Add a question to the database"""
    if ('entry' in request.form):
        q = Question(question=request.form['entry'], aproved="yes")
        q.save()
    return redirect(url_for('home'))

def question():
    """template for question"""
    return render_template('question_clean.html')
    


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

