from flask import Flask, render_template, request, redirect, flash, session
from mysqlconnection import MySQLConnector
import re 
import json

from flask.ext.bcrypt import Bcrypt
from datetime import datetime, timedelta

mysql = MySQLConnector('persona_db')
app = Flask (__name__)
bcrypt = Bcrypt(app)
app.secret_key = "SecretKeyHere"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$') 

#Home page 
@app.route ('/')
def index():
    # Display log in page if not logged in
    if not session.get('userid') or not session['userid']: #second one means if session['userid'] = False
        return render_template('index.html')

    # If logged in already, redirect to dashboard (according to admin level)
    current_user = mysql.fetch("SELECT * FROM users WHERE id = {}".format(session['userid']))
    print current_user
    return render_template('index.html', current_user = current_user)


#Authenticate user if they login
@app.route ('/login', methods=['POST'])
def authenticate_login():

    print "In authenticate_login function"

    data_requested = request.data
    json_data = json.loads(data_requested)

    print json_data

    email = json_data['email']
    password = json_data['password']
    

    #Check if both fields are inputted
    if len(email) ==0 or len(password) == 0:
        flash (u'Please enter your email and password to login','login')
        return redirect ('/')

    #Validate email
    if not EMAIL_REGEX.match(email): 
        print "Validate email error"
        flash (u'Invalid email address','email_login')
        return redirect ('/')

    #Check if user exists with the given email and password
    current_user = mysql.fetch("SELECT * FROM users WHERE email = '{}'".format(email))
    print "CURRENT USER", current_user
    if len(current_user) == 0:
        print "Wrong email"
        flash (u'Wrong email or password entered. Please try again','login')
        return redirect ('/')

    if not bcrypt.check_password_hash(current_user[0]['password'], password):
        print "Wrong password"
        flash (u'Wrong email or password entered. Please try again!','login')
        return redirect ('/')


    #At this point everything has been validated and passwords checked
    session['login'] = True
    session['userid']= current_user[0]['id']

    print "session login" + session['login']
    print "session userid" + session['userid']

    return redirect ('/')




#Register user
@app.route ('/register', methods=['POST'])
def add_user_login():
        print "In add_user_login function"
        print "Request data" + request.data
        data_requested = request.data
        json_data = json.loads(data_requested)
        print "Json loads"
        print json_data

        # register_info = {
        #     "firstname": json_data['firstname'],
        #     "lastname": json_data['lastname'],
        #     "username": json_data['username'],
        #     "email": json_data['email'], 
        #     "password": json_data['password'],
        #     "conf_password": json_data['conf_password'],
        #     "helper": json_data['helper'],
        #     "zipcode": json_data['zipcode'],
        #     "description": json_data['description']
        # }

       
        firstname = str(json_data['firstname'])
        lastname = str(json_data['lastname'])
        username = str(json_data['username'])
        email = json_data['email']
        password = str(json_data['password'])
        conf_password = json_data['conf_password']
        helper = json_data['helper']
        zipcode = json_data['zipcode']
        description = json_data['description']
        


        # register_status = self.models['User'].register(register_info)
        error_dict = {}
        error = False

        #Check if all fields are inputted, return right away if any field is missing
        if len(firstname)==0 or len(lastname) ==0 or len(email) ==0 or len(password)==0 or len(conf_password)==0:
            error_dict['register'] = "All fields are required! Please try again."
            error = True
            return {"status" : False, "error_dict": error_dict}

        #Check first name is atleast 2 chars
        if len(firstname) < 2:
            error_dict['firstname'] = "First Name must be atleast 2 characters. Please try again."
            error = True

        elif str.isalpha(firstname)==False:
            error_dict['firstname'] = "Names must not contain numbers. Please try again."
            error = True

        #Check last name is atleast 2 chars & all characters
        if len(lastname) < 2:
            error_dict['lastname'] = "Last name must be atleast 2 characters. Please try again."
            error = True

        elif str.isalpha(lastname)==False:
            error_dict['lastname'] = "Last name must not contain numbers. Please try again."
            error = True

        #Validate email
        if not EMAIL_REGEX.match(email):
            error_dict['email_register'] = "Invalid email address."
            error = True

        #Check if email already exists in database
        user_email = mysql.fetch("SELECT * FROM users WHERE email = '{}'".format(email))
        if len(user_email) > 0:
            error_dict['email_register'] = "Email address already exists. Please try registering with another email, or login using this email."
            error = True


        #Validate password
        num_in_pass = False
        upper_in_pass = False
        for char in str(password):
            if str.isupper(char):
                upper_in_pass = True
            if str.isdigit(char):
                num_in_pass = True

        if len(password) < 8:
            error_dict['password_register'] = "Password must be 8 characters."
            error = True

        elif password != conf_password:
            error_dict['password_register'] = "Passwords do not match."
            error = True

        elif num_in_pass == False or upper_in_pass == False:
            error_dict['password_register'] = "Please use atleast 1 uppercase letter and 1 numeric value in your password."
            error = True


        #Check if there were any errors in the previous validation process
        # if error == True:
        #     return redirect ('/')
            # return {"status" : False, "error_dict": error_dict}

        pw_hash = bcrypt.generate_password_hash(password)
        insert_query = "INSERT INTO users (first_name, last_name, username, email, password, helper, zipcode, description, created_at, updated_at) VALUES ('{}','{}','{}','{}','{}', '{}', '{}', '{}', NOW(), NOW())".format(firstname, lastname, username, email, pw_hash, helper, zipcode, description)
        mysql.run_mysql_query(insert_query)
 

        # #Flash errors if registration fails
        # if register_status['status'] == False:
        #     error_dict = register_status['error_dict']
        #     for key,val in error_dict.items():
        #         flash(val, key)
        #     return redirect ('/register')


        # #Log in the user if user is registered successfully
        # else:

        #Get the last id from the users table and set the session['id']
        get_id_query = "SELECT id FROM users ORDER BY id DESC LIMIT 1"  
        id_col = mysql.fetch(get_id_query)
        registered_id = id_col[0]['id']
        session['userid'] = registered_id

        if helper == 1:
            realestate = json_data['helper']
            finances = json_data['finances']
            medicalcare = json_data['medicalcare']
            automobile = json_data['automobile']
            lang_tutor = json_data['lang_tutor']
            lang_translator = json_data['lang_translator']
            social = json_data['social']
            previous_newcomer = json_data['previous_newcomer']

            helper_insert_query = "INSERT INTO helper (user_id, realestate, finances, medicalcare, automobile, lang_tutor, lang_translator, social, previous_newcomer, created_at, updated_at) VALUES ('{}','{}','{}','{}','{}','{}', '{}', '{}', '{}', NOW(), NOW())".format(registered_id, realestate, finances, medicalcare, automobile, lang_tutor, lang_translator, social, previous_newcomer)
            mysql.run_mysql_query(helper_insert_query)

        else:
            date_entry = json_data['date_entry']
            newcomer_insert_query = "INSERT INTO newcomer (user_id, date_entry, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(registered_id, date_entry)
            mysql.run_mysql_query(newcomer_insert_query)

        
        # return {"status": True, "id":last_user_id}

        return redirect ('/')



app.run(debug = True)


