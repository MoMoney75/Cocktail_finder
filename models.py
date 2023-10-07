from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete, update, ForeignKey

bcrypt = Bcrypt()
db = SQLAlchemy()
def connect_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()

class User(db.Model):
     __tablename__ = "users"

     user_id = db.Column(db.Integer, primary_key=True)
     first_name = db.Column(db.Text, unique=False, nullable = False)
     last_name = db.Column(db.Text, unique=False, nullable=False)
     username = db.Column(db.Text, unique=False, nullable=False)
     password = db.Column(db.Text, unique=False, nullable=False)
     favorites = db.relationship('Favorites', backref='user', cascade='all, delete-orphan')

class Favorites(db.Model):
     __tablename__ = "favorites"

     favorite_id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, ForeignKey('users.user_id'))
     cocktail_id =db.Column(db.Integer, unique=False)
     __table_args__ = (db.UniqueConstraint('user_id', 'cocktail_id'),)
