from flask import Flask, render_template, session, flash, redirect
from flask_bcrypt import Bcrypt
from forms import SearchIngredient, Login, SignUp,Edit_Form
from models import User, Favorites, connect_db,db
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

import requests


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wkebvnoe:LZQUWP5OqP6O6vLl1y1Gfjy3GGVbnb78@bubble.db.elephantsql.com/wkebvnoe'

with app.app_context():
    connect_db(app)


base_url = f'https://www.thecocktaildb.com/api/json/v2/{API_KEY}'


@app.route('/')
def home_page():
    """show landing page"""
    return render_template('home.html')

@app.route('/login', methods=["GET","POST"])
def login():
    """handle user login"""
    form = Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password,password):
            session['curr_user'] = user.username
            session['user_id'] = user.user_id
            flash(F"Welcome back {user.first_name}!")
            return redirect('/search')

        else:
            flash('The username or password you entered is incorrect')
            return redirect('/login')
        
    return render_template("login.html", form=form)
        

@app.route('/logout')
def logout():
    """handle loging user out"""
    session.pop('curr_user')
    session.pop('user_id')
    flash('Logout successful!')
    return redirect('/')
        
@app.route('/signup', methods=["GET", "POST"])
def signup():
    """render signup form"""
    form = SignUp()

    return render_template('signup.html', form=form)

@app.route('/signup/handle', methods=["GET", "POST"])
def handle_signup():
    """handle creating user and redirect to search page if successfull"""
    form = SignUp()
    if form.validate_on_submit():
        first_name=form.first_name.data
        last_name=form.last_name.data
        username=form.username.data
        password=form.password.data
        hashed_password = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_password.decode("utf8")

        user = User(first_name=first_name,last_name=last_name,username=username,password=hashed_utf8)
   
        db.session.add(user)
        db.session.commit()
        session['curr_user'] = user.username
        session['user_id'] = user.user_id
        flash(F"Welcome {user.first_name}!")
        return redirect('/search')

    else:
        return redirect('/signup')
    

@app.route('/<int:user_id>/delete', methods=["GET","POST"])
def delete_user(user_id):
    """handle delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Account has been successfully deactivated", "info")

    return redirect('/')
    
@app.route('/search')
def show_searchForm():
    """render cocktail search form"""
    if 'curr_user' in session:
        user_id = session['user_id'] 
        form = SearchIngredient()
        return render_template('search_ingredients.html', form=form, user_id=user_id)

    else: 
        flash('You must be logged in to see this page!')
        return redirect('/')

    

@app.route('/handle_search', methods=["POST"])
def get_cocktails():
    form = SearchIngredient()
    user_id = session['user_id']
    user = User.query.get_or_404(user_id)

    drinks_ids = [] #stored the id of each drink
    drink_data = [] #stores each drink
    user_favorites =[] #store user favorite ids

    for data in user.favorites:
        user_favorites.append(data.cocktail_id)
    

    #get results for cocktails searching by ingredients 
    if "curr_user" in session:
        if form.validate_on_submit():
            ingredients1 = form.ingredients1.data
            ingredients2 = form.ingredients2.data
            ingredients3 = form.ingredients3.data
            ingredients = [ingredients1]

            #if user inputs additional ingredients(optional)
            if ingredients2:
                ingredients.append(ingredients2)
            if ingredients3:
                ingredients.append(ingredients3)

            recipe = ','.join(ingredients)
            response = requests.get(f"{base_url}/filter.php?i={recipe}")
            print(f"STATUSCODE {response.status_code}")
            print(f" MY API KEY: {API_KEY}")
            print(f"MY BASE URL:{base_url}")
            data = response.json()
            
            print(data)
            

            if data == {'drinks': 'None Found'}:
                flash("No drinks found with all of the ingredients, Please try a different ingredient")
                return redirect('/search')

            else:
                #loop through results, get drink ids of every drink
                for drink in data['drinks']:
                    drink_id = drink['idDrink']
                    drinks_ids.append(drink_id)

                    #use drink_id from the results above. Plug in drink_id to get full details
                    #about cocktail
                for drink in drinks_ids:
                    data = requests.get(F"{base_url}/lookup.php?i={drink}")
                    cocktail_details = data.json()

                    for drinks in cocktail_details['drinks']:
                        name = drinks['strDrink']
                        drink_data.append({"name": name, "details": drinks}) 

                
                return render_template('search_ingredients_result.html',drink_data=drink_data,user=user)
        
    else:
        flash('Must be logged in to view this page!')
        return redirect('/')
    


@app.route('/details/<int:drink_id>', methods=['GET'])
def show_details(drink_id):
    """show indivdual drink details searcherd by drink id"""
    user_id = session['user_id']

    if "curr_user" in session:
        response = requests.get(f"{base_url}/lookup.php?i={drink_id}")
        data = response.json()
        return render_template('drink_details.html', data=data, user_id=user_id)
    
    else:
        flash("You must be logged in to view this page!")
        return redirect('/')
    

@app.route('/<int:drink_id>/add_favorites', methods=['POST'])
def add_favorites(drink_id):
    """hanlde adding user favorites"""
    if "curr_user" in session:
        response = requests.get(f"{base_url}/lookup.php?i={drink_id}")
        data = response.json()
    
        for id in data['drinks']:
            cocktail_id = id['idDrink']
        
        user_id = session['user_id']
        new_favorite = Favorites(user_id=user_id,cocktail_id=cocktail_id)
               
        try:
             db.session.add(new_favorite)
             db.session.commit()
             flash("Cocktail successfully added to your favorites!")
             return redirect(f"/{user_id}/favorites")
             
        except:
            db.session.rollback()
            flash("Cocktail is already in your favorites!")
            return redirect (f"/{user_id}/favorites")

    else: 
        flash('You must be logged in to see this page!')
        return redirect('/')
    

@app.route('/<int:cocktail_id>/delete_favorite', methods=["POST"])
def delete_favorite(cocktail_id):
    """delete a user favorite from favorites"""
    if "curr_user" in session:
        user_id = session['user_id']
        cocktail = Favorites.query.filter_by(user_id=user_id, cocktail_id=cocktail_id).first()

        db.session.delete(cocktail)
        db.session.commit()
        flash('Cocktail successfully deleted!')

        return redirect(F"/{user_id}/favorites")
    
    else:
        flash('You must be logged in to see this page!')
        return redirect('/')
        

@app.route('/<int:user_id>/favorites', methods=['GET','POST'])
def show_favorites(user_id):
    """show all of a user's favorites"""
    if "curr_user" in session:
        user = User.query.get_or_404(user_id)
        favorites = user.favorites
        drink_data = []

        for favorite in favorites:
            cocktail_id = favorite.cocktail_id
            response = requests.get(f"{base_url}/lookup.php?i={cocktail_id}")
            data = response.json()

            for drinks in data['drinks']:
                drink_name = drinks['strDrink']
                drink_data.append({"name": drink_name, "details": drinks})


        return render_template('favorites.html', user=user, drink_data=drink_data, favorites = favorites)
    
    else:
        flash('You must be logged in to see this page!')
        return redirect('/')
        

@app.route('/<int:user_id>/edit',methods=["GET","POST"])
def edit_user(user_id):
    """edit user profile"""
    form = Edit_Form()
    user = User.query.get_or_404(user_id)
    if "curr_user" in session:
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.username = form.username.data
            password = form.password.data
            hashed_password = bcrypt.generate_password_hash(password)
            hashed_utf8 = hashed_password.decode("utf8")
            user.password= hashed_utf8

            db.session.add(user)
            db.session.commit()

            session['curr_user'] = user.username
            session['user_id'] = user.user_id
            flash("User settings successfully updated!")
            return redirect('/search')
        
    else:
        flash("You must be logged in to view this page!")
        return redirect('/')


    return render_template("edit_user.html",user=user,form=form)
    

