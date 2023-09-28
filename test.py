from app import app
from flask import Flask
from flask_bcrypt import Bcrypt
from models import User, Favorites, db
import unittest

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cocktail_db'
app.config['WTF_CSRF_ENABLED'] = False  # no CSRF during tests
app.config["TESTING"] = True

class test_app(unittest.TestCase):
    def setUp(self):
        """things to do before every test"""

        self.client = app.test_client()
        """CREATE A USER FOR TESTING PURPOSES"""

        test_user1 = User(first_name="tester1111", 
                     last_name="lastname1111", 
                     username="tester1111", 
                     password=bcrypt.generate_password_hash("password123").decode("utf-8"))
        
        
        db.session.add(test_user1)
        db.session.commit()

    def tearDown(self):
        """stuff to do after every test"""
        tester1111 = User.query.filter_by(username="tester1111").first()

        db.session.delete(tester1111)
        db.session.commit()

    def test_home_page(self):
        """Testing to see if home page is rendered"""
        with app.test_client() as client:
             response = client.get('/')
             html = response.get_data(as_text=True)

             self.assertEqual(response.status_code,200)
             self.assertIn("<h1>Welcome to Cocktail Finder</h1>",html)


    
    def test_signup_page(self):
        """Testing to see if signup page is rendered"""
        with app.test_client() as client:
            response = client.get('/signup')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code,200)
            self.assertIn("first name",html)
            self.assertIn("last name",html)
            self.assertIn("username",html)
            self.assertIn("password",html)

    
    def test_create_new_user(self):
        """Testing signing up new user"""
        password = "password999"
        with app.test_client() as client:
            
            data = {"first_name" :"Mo", 
                    "last_name" :"Silba" , 
                    "username" :"Tester_test", 
                    "password" : password
                    }
            response = client.post('/signup/handle',data=data, follow_redirects=True)
            user = User.query.filter_by(username="Tester_test").first()

            self.assertEqual(response.status_code,200)
            self.assertIsNotNone(user)
            self.assertEqual(user.username,"Tester_test")
            self.assertEqual(user.first_name,"Mo")

    def test_login_form(self):
        """Testing login form is rendered"""
        with app.test_client() as self.client:
            response = self.client.get('/login', follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertIn("username",html)
            self.assertIn("password", html)
            self.assertEqual(response.status_code, 200)

    def test_loggin_user(self):
        """testing user is logged in"""
        with app.test_client() as self.client:
            user = User.query.filter_by(username="tester1111").first()
            data = {"username" : user.username , "password": "password123" }

            response = self.client.post('/login/handle', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code,200)
            self.assertIn("Search for a cocktail by ingredients!", html)
            self.assertIn("search for drink", html)

    # def test_search_page(self):
    #     """test to see rendered results from API"""
    #     with app.test_client() as client:
    #         with client.session_transaction() as session:
    #             session['curr_user'] = "tester1111"
    #             session["user_id"] = 2

    #         data = {"ingredients1" : "lime", "ingredients2":"tequila"}
    #         response = client.post('/handle_search_ingredients', data=data ,follow_redirects=True)
    #         html = response.get_data(as_text=True)
    #         print(html)

    #         self.assertEqual(response.status_code,200)


    # def test_add_favorite(self):
    #     user = User.query.filter_by(username="tester1111").first()
    #     with app.test_client() as client:
    #         with client.session_transaction() as session:
    #             session['curr_user'] = user.username
    #             session["user_id"] = user.user_id

    #         data = {"favorite_id": 100, "user_id": user.user_id, "cocktail_id" : 11007}
            
    #         response = client.post('/add_favorites',data=data,follow_redirects=True)
    #         favorite = Favorites.query.filter_by(user_id = user.user_id)
    #         print(response)
    #         print(favorite)





