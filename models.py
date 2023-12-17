from __init__ import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(email):
    return Users.query.get(email))

class Users(db.Model, UserMixin):
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), nullable=False, primary_key=True)
    password = db.Column(db.String(60), nullable=False)
