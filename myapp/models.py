from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(156), unique= True)
    password =  db.Column(db.String(120))
    name = db.Column(db.String(120))

    blogs = db.relationship('Blog', backref='author', lazy=True)

