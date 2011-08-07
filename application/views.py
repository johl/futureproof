"""
views.py

URL routes and handlers

"""

from flask import render_template, url_for, redirect, request
from models import Question
from decimal import Decimal
from types import *
import random
TWOPLACES = Decimal(10) ** -2

def home():
    questions = Question.gql( "WHERE aproved = 'yes'" ).fetch(limit=100)
    if (len(questions) != 0 and questions != None):
        random.shuffle(questions)
        top_yes = Question.gql( "WHERE aproved = 'yes' AND vote_yes !=0 ORDER BY vote_yes DESC" ).fetch(limit=3)
        top_no = Question.gql( "WHERE aproved = 'yes' AND vote_no!=0 ORDER BY vote_no DESC" ).fetch(limit=3)
    else:
        """
        Nothing in the database, let's fill it up with some stock questions.
        """
        stock_questions = (
                "have DVDs",
                "have desktop computers",
                "have optical media in the same size and shape as CDs and DVDs",
                "have free bags with a purchase from a store",
                "have cheap wine in bottles",
                "have large grocery stores that you make orders from",
                "have CDs",
                "have written signatures on credit card receipts",
                "have paper receipts for purchases",
                "have large grocery stores that you visit in person",
                "have IPv4",
                "have credit cards based upon magnetic strips",
                "have voice-only phone calls",
                "have IPv6",
                "have refridgerator magnets",
                "have corks actually made out of cork",
                "have broadcast television",
            )
        for question in stock_questions:
            q = Question(question=question, vote_yes=0, vote_no=0, total=0, aproved="yes")
            q.save()
            questions.append(q)
            top_yes = questions
            top_no = questions
    top_yes = [i for i in top_yes if i.vote_yes != 0]
    top_yes = [
                {
                'question': entry.question,
                'key': entry.key(),
                'total': entry.total,
                'style': "style-" + str(int(float(Decimal(str(float(1.0*entry.vote_yes/entry.total)*100)).quantize(TWOPLACES)))),
                'percent': float(Decimal(str(float(1.0*entry.vote_yes/entry.total)*100)).quantize(TWOPLACES))
                } for entry in top_yes if entry.total != 0]
    top_yes.sort(lambda x, y: cmp(x['percent'], y['percent']), reverse=True)
    top_no = [i for i in top_no if i.vote_no != 0]
    top_no = [
                {
                'question': entry.question,
                'key': entry.key(),
                'total': entry.total,
                'style': "style-" + str(100- int(float(Decimal(str(float(1.0*entry.vote_no/entry.total)*100)).quantize(TWOPLACES)))),
                'percent': 100.00 - float(Decimal(str(float(1.0*entry.vote_no/entry.total)*100)).quantize(TWOPLACES))
                } for entry in top_no if entry.total != 0]
    top_no.sort(lambda x, y: cmp(x['percent'], y['percent']))
    return render_template('index.html', questions=questions, top_yes=top_yes, top_no=top_no)
    

def fill():
    stock_questions = (
            "have DVDs",
            "have desktop computers",
            "have optical media in the same size and shape as CDs and DVDs",
            "have free bags with a purchase from a store",
            "have cheap wine in bottles",
            "have large grocery stores that you make orders from",
            "have CDs",
            "have written signatures on credit card receipts",
            "have paper receipts for purchases",
            "have large grocery stores that you visit in person",
            "have IPv4",
            "have credit cards based upon magnetic strips",
            "have voice-only phone calls",
            "have IPv6",
            "have refridgerator magnets",
            "have corks actually made out of cork",
            "have broadcast television",
        )
    for question in stock_questions:
        q = Question(question=question, vote_yes=0, vote_no=0, total=0, aproved="yes")
        q.save()
    
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
    import urllib
    escaped_url=urllib.quote_plus("http://www.isitfutureproof.com/question/" + qid)
    if ('vote_value' in request.form):
        agree = "didn't tell us if you agree or disagree"
        question = Question.get(qid)
        if (question.total == None):
            question.total = 0
        if (question.vote_no == None):
            question.vote_no = 0
        if (question.vote_yes == None):
            question.vote_yes = 0
        question.total = question.total + 1
        if (request.form['vote_value'] == "yes"):
            question.vote_yes = question.vote_yes +1
            agree = "disagree"
        if (request.form['vote_value'] == "no"):
            question.vote_no = question.vote_no +1
            agree = "agree"
        question.save()
        question = Question.get(qid)
        percent = 0
        stylepercent = "style-0"
        if (question.total > 0):
            percent = float(Decimal(str(float(1.0*question.vote_no/question.total)*100)).quantize(TWOPLACES))
            stylepercent = "style-" + str(int(percent))
        return render_template('question_result.html', escaped_url=escaped_url, qid=qid, question=question.question, percent=percent, total=question.total, agreed=agree, stylepercent=stylepercent)
    else:
        question = Question.get(qid)
        return render_template('question_clean.html', qid=qid, escaped_url=escaped_url, question=question.question)

def leaderboard():
    """template for leaderboard"""
    return render_template('leaderboard.html')


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

