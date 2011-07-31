"""
views.py

URL routes and handlers

"""

from flask import render_template, url_for, redirect, request
from models import Question
from decimal import Decimal
from types import *
import random

def home():
    questions = Question.gql( "WHERE aproved = 'yes'" ).fetch(limit=100)
    if (not questions == None):
        random.shuffle(questions)
        return render_template('index.html', questions=questions)
    else:
        return render_template('index.html')

def add_question():
    """Add a question to the database"""
    if ('entry' in request.form):
        q = Question(question=request.form['entry'], aproved="yes")
        q.save()
    return redirect(url_for('home'))
    
def random_question(qid=None):
    """Return a random question that isn't the one this was linked from"""
    questions = Question.gql( "WHERE aproved = 'yes'" ).fetch(limit=100)
    if (not questions == None):
        questions = [question for question in questions if question.key() != qid]
        random.shuffle(questions)
        question = questions.pop()
        return redirect("/question/%s/" % question.key())

def question_result(qid=None):
    if ('vote_value' in request.form):
        agree = "didn't tell us if you agree or disagree"
        question = Question.get(qid)
        if (question.total == None):
            question.total = 0
        if (question.no == None):
            question.no = 0
        if (question.yes == None):
            question.yes = 0
        question.total = question.total + 1
        if (request.form['vote_value'] == "yes"):
            question.yes = question.yes +1
            agree = "disagree"
        if (request.form['vote_value'] == "no"):
            question.no = question.no +1
            agree = "agree"
        question.save()
        question = Question.get(qid)
        percent = 0
        stylepercent = "style-0"
        if (question.total > 0):
            TWOPLACES = Decimal(10) ** -2
            percent = float(Decimal(str(float(1.0*question.no/question.total)*100)).quantize(TWOPLACES))
            stylepercent = "style-" + str(int(percent))
        return render_template('question_result.html', qid=qid, question=question.question, percent=percent, total=question.total, agreed=agree, stylepercent=stylepercent)
    else:
        question = Question.get(qid)
        return render_template('question_clean.html', qid=qid, question=question.question)

def leaderboard():
    """template for leaderboard"""
    return render_template('leaderboard.html')


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

