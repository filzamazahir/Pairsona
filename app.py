from flask import Flask, render_template, request, redirect, flash, session, jsonify
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
    print current_user[0]
    print type(current_user[0])
    return jsonify(**current_user[0])
    # return render_template('index.html', current_user = current_user)



#################################################################################


#Login
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

    print "session login", session['login']
    print "session userid", session['userid']

    return redirect ('/')



#Logoff
@app.route ('/logoff')
def logoff ():
    session['login'] = False
    session.pop('userid')

    return redirect ('/')


#################################################################################


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
        country_origin = json_data['country_origin']
        


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
        insert_query = "INSERT INTO users (first_name, last_name, username, email, password, helper, zipcode, description, country_origin, created_at, updated_at) VALUES ('{}','{}','{}','{}','{}', '{}', '{}', '{}','{}', NOW(), NOW())".format(firstname, lastname, username, email, pw_hash, helper, zipcode, description, country_origin)
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


#################################################################################

#Search Query
@app.route('/search/<helper_bool>/<zipcode>')
def search_people (helper_bool, zipcode):
    helper_bool = int(helper_bool)
    zipcode = int(zipcode)
    if helper_bool == 1:
        users = mysql.fetch("SELECT * FROM users WHERE helper = 0 AND zipcode = {}".format(zipcode))
    else:
        users = mysql.fetch("SELECT * FROM users WHERE helper = 1 AND zipcode = {}".format(zipcode))
    
    print users
    users_dict = {"searchresults" : users}

    print users_dict
    print type(users_dict)

    return jsonify(**users_dict)

# NOTE: The helper doesn't get any filters to look for newcomers needing help

#Filter Query
@app.route('/search/0/<zipcode>', methods=['POST'])
def filter_search (zipcode):
    zipcode = int(zipcode)
    print zipcode

    filters_requested = request.data
    json_filters = json.loads(filters_requested)

    realestate = json_filters['realestate']
    finances = json_filters['finances']
    medicalcare = json_filters['medicalcare']
    automobile = json_filters['automobile']
    lang_tutor = json_filters['lang_tutor']
    lang_translator = json_filters['lang_translator']
    social = json_filters['social']
    previous_newcomer = json_filters['previous_newcomer']

    query = "SELECT * FROM users LEFT JOIN helper ON users.id = helper.user_id WHERE helper = 1 AND zipcode = {}".format(zipcode)
    additions = "";
        
    if realestate:
        additions += " AND realestate = {}".format(realestate)
    if finances:
        additions += " AND finances = {}".format(finances)          
    if medicalcare:
        additions += " AND medicalcare = {}".format(medicalcare)
    if automobile:
        additions += " AND automobile = {}".format(automobile)
    if lang_tutor:
        additions += " AND lang_tutor = {}".format(lang_tutor)
    if lang_translator:
        additions += " AND lang_translator = {}".format(lang_translator)
    if social:
        additions += " AND social = {}".format(social)
    if previous_newcomer:
        additions += " AND previous_newcomer = {}".format(previous_newcomer)
        
    if len(additions) > 0:
        query += additions

    # users = mysql.fetch("SELECT * FROM users LEFT JOIN helper ON users.id = helper.user_id WHERE helper = 1 AND zipcode = {} AND realestate = {} AND finances = {} AND medicalcare = {} AND automobile = {} AND lang_tutor = {} AND lang_translator = {} AND social = {} AND previous_newcomer".format(zipcode, realestate, finances, medicalcare, automobile, lang_tutor, lang_translator, social, previous_newcomer))
    users = mysql.fetch(query)
    print users
    users_dict = {"searchresults" : users}
    return jsonify(**users_dict)


# Connection Method
@app.route('/connect', methods=['POST'])
def add_connection ():
      

    connection_attributes = request.data
    json_connection_attributes = json.loads(connection_attributes)

    helper_id = json_connection_attributes['helper_id']
    newcomer_id = json_connection_attributes['newcomer_id']
   

    mysql.run_mysql_query("INSERT INTO connections (helper_id, newcomer_id, created_at, updated_at) values ('{}','{}',NOW(),NOW())".format(helper_id, newcomer_id))
    
    return redirect ('/')



@app.route('/connections/<user_id>')
def view_connections (user_id):
    
    user_id = int(user_id)
    # is_helper = int(ishelper)
    
    # connection_attributes = request.data
    # json_connection_attributes = json.loads(connection_attributes)

    # user_id = json_connection_attributes['user_id']
    # is_helper = json_connection_attributes['is_helper']
    current_user = mysql.fetch("SELECT * FROM users WHERE id = {}".format(user_id))
    print "CURRENT USER"
    print current_user[0]
    is_helper = current_user[0]['helper']
    

    if (is_helper):
        connections = mysql.fetch("SELECT * from connections LEFT JOIN users ON users.id = connections.newcomer_id where helper_id = {}".format(user_id))
    
    else: 
        connections = mysql.fetch("SELECT * from connections LEFT JOIN users  ON users.id = connections.helper_id where new_comer = {}".format(user_id))

    print "CONNECTIONS"
    print connections
    connection_dict = {"connection_list" : connections}
    return jsonify(**connection_dict)


@app.route('/invites', methods=['POST'])
def add_invites ():
    
    invite_attributes = request.data
    json_invite_attributes = json.loads(invite_attributes)

    inviter_id = json_invite_attributes['inviter_id']
    invited_id = json_invite_attributes['invited_id']
   

    mysql.run_mysql_query("INSERT INTO invitations (inviter_id, invited_id) values ('{}','{}')".format(inviter_id, invited_id))
    
    return redirect ('/')



@app.route('/invites/<user_id>')
def view_invites (user_id):
      
    user_id = int(user_id)
    # invite_attributes = request.data
    # json_invite_attributes = json.loads(invite_attributes)

    # user_id = json_invite_attributes['user_id']


    invites = mysql.fetch("SELECT * from invitations LEFT JOIN users ON users.id = invitations.inviter_id where invited_id = {}".format(user_id))
    # SELECT * from invitations LEFT JOIN users ON users.id = invitations.inviter_id where invited_id = 2

    
    invites_dict = {"invites_list" : invites}
    return jsonify(**invites_dict)



app.run(debug = True)


