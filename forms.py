from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import  Length, InputRequired, Optional

class Login(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class SignUp(FlaskForm):
    first_name=StringField('First name',validators=[InputRequired()])
    last_name=StringField('Last name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=8,max=16, message="username must be between 8 and 16 characters long")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=13,message="password must be between 8 and 13 characters long")])
    
class SearchIngredient(FlaskForm):
    ingredients1 = StringField('First Ingredient', validators=[InputRequired()])
    ingredients2 = StringField('Second Ingredient(Optional)', validators=[Optional()])
    ingredients3 = StringField('Third Ingredient (Optional)', validators=[Optional()])

class Edit_Form(FlaskForm):
    first_name=StringField('First name',validators=[InputRequired()])
    last_name=StringField('Last name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=8,max=16, message="username must be between 8 and 16 characters long")])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=13,message="password must be between 8 and 13 characters long")])
    
