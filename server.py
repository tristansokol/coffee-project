""" Server for the Coffee Project App"""

from flask import (Flask, render_template, request, session, redirect, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db
import crud

# Throw errors for undefined variables in Jinja2
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# ROUTES
@app.route('/')
def root():
    """Render the one page web app that's made w/ React"""
    return render_template('root.html')


# CATCH-ALL ROUTE
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('root.html')


# API ENDPOINTS
@app.route('/api/logout', methods=['POST'])
def process_logout():
    # Deletes user from session (log user out)
    del session['user_id']

    return jsonify({'message': "Logged Out"})

@app.route('/api/login', methods=['POST'])
def process_login():
    # Get data from user login form input
    # expecting {"email": "glo@gmail.com", "password": "real secret like"}
    
    print("************** In the server *****************")

    data = request.get_json()
    email = data['email']
    password = data['password']

    # Use email to check if this user is in the database
    user = crud.get_user_by_email(email=email)

    # If they're in the database, and passwords match, log them in
    if user and password == user.password:
        # Add user_id to the session (log user in)
        session["user_id"] = user.user_id
        status = 'success'
        message = 'Logged in! Success!'
        
    else:
        status = 'error'
        message = 'Incorrect email or password. Try again'
        
    return jsonify({'status': status, 'message':message})

@app.route('/api/create-account', methods=['POST'])
def create_new_account():
    # Get data from user to create a new account

    # expecting {"email": "glo@gmail.com", "password": "real secret like",
    # "homeZipcode": "90291"}
    print("************** In the server *****************")

    data = request.get_json()
    email = data['email']
    password = data['password']
    home_zipcode = data['homeZipcode']

    # Use email to check if this user is in the database
    user = crud.get_user_by_email(email=email)

    # If they're in the database, send message that they have an account
    if user:
        status = 'error'
        message = 'This email has an existing account. Try logging in.'
        
    else:
        # If they user is not in the db, create them!
        crud.create_user(email=email, password=password, home_zipcode=home_zipcode)
        status = 'success'
        message = 'Account created! Please log in.'
        
    return jsonify({'status': status, 'message':message})

@app.route('/api/get-user-information')
def get_user_info():
    # Get all information about a user when they're logged in

    # Get the user_id from the session
    user_id = session.get("user_id")

    # Query the db for the user
    user = crud.get_user_by_id(user_id)
    zipcode = user.home_zipcode

    # Get all the user's user features
    user_features = crud.get_all_ufs_for_user(user)

    return jsonify({'zipcode': zipcode})







if __name__ == '__main__':
    # Connect to db first, then app can access it.
    # Set debug to True before accessing the Debug Toolbar
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host='0.0.0.0')