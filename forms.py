from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import  Length, InputRequired, Optional

class Login(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

class SignUp(FlaskForm):
    first_name=StringField('first name',validators=[InputRequired()])
    last_name=StringField('last name', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired(), Length(min=8,max=16, message="username must be between 8 and 16 characters long")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=13,message="password must be between 8 and 13 characters long")])
    

class SearchIngredient(FlaskForm):
    ingredients1 = StringField('Ingredients', validators=[InputRequired()])
    ingredients2 = StringField('optional', validators=[Optional()])
    ingredients3 = StringField('optional', validators=[Optional()])

class Edit_Form(FlaskForm):
    first_name=StringField('first name',validators=[InputRequired()])
    last_name=StringField('last name', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired(), Length(min=8,max=16, message="username must be between 8 and 16 characters long")])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=13,message="password must be between 8 and 13 characters long")])
    
