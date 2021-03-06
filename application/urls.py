"""
urls.py

URL dispatch route mappings and error handlers

"""

from flask import render_template

from application import app
from application import views


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

app.add_url_rule('/', 'home', view_func=views.home)
app.add_url_rule('/fill', 'fill', view_func=views.fill)
app.add_url_rule('/question/<qid>/', 'question_result', view_func=views.question_result, methods=['POST'])
app.add_url_rule('/question/<qid>/', 'question_result', view_func=views.question_result)
app.add_url_rule('/next/<qid>/', 'random_question', view_func=views.random_question)
app.add_url_rule('/leaderboard', 'leaderboard', view_func=views.leaderboard)
app.add_url_rule('/add', 'add_question', view_func=views.add_question, methods=['POST'])  

## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

