"""
views.py

URL routes and handlers

"""


from google.appengine.api import users

from flask import render_template, flash, url_for, redirect

from models import ExampleModel
from decorators import login_required, admin_required
from forms import ExampleForm


def home():
    return redirect(url_for('list_examples'))


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username


def list_examples():
    """List all examples"""
    examples = ExampleModel.all()
    return render_template('list_examples.html', examples=examples)


@login_required
def new_example():
    """Add a new example"""
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
                    example_id = form.example_id.data,
                    example_title = form.example_title.data,
                    added_by = users.get_current_user()
                    )
        example.put()
        flash(u'Example successfully saved.', 'success')
        return redirect(url_for('list_examples'))
    return render_template('new_example.html', form=form)


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

