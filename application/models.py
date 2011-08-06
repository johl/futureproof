"""
models.py

App Engine datastore models

"""
from google.appengine.ext import db


# class ExampleModel(db.Model):
#     """Example Model"""
#     example_id = db.StringProperty(required=True)
#     example_title = db.StringProperty(required=True)
#     added_by = db.UserProperty()
#     timestamp = db.DateTimeProperty(auto_now_add=True)
    
class Question(db.Model):
    """Question Model"""
    question = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    aproved = db.StringProperty(required=True)
    vote_yes = db.IntegerProperty()
    vote_no = db.IntegerProperty()
    total = db.IntegerProperty()

