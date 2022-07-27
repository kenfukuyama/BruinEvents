# imports
from flask_app import app, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import pprint
pp = pprint.PrettyPrinter(indent=4)

from flask_app.models.user import User


# ! Home  - direct user to login 
@app.route('/')
def index():
    # check if they are logged in
    if "user_id" in session:
        return redirect('/events/dashboard')
    # render login
    return render_template('user_login.html')

# ! Register Page
@app.route('/users/register')
def users_register_page():
    # render register page
    return render_template('user_register.html')


# ! Register POST
@app.route('/users/register', methods=['POST'])
def register_user():
    # validate register forms
    if not User.validate_user_register(request.form):
        return redirect('/users/register')
    # store to data for sql query
    data = {    
        "name": request.form['name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    # create session for registered user
    session['user_id']  = str(User.create(data))
    session['name'] =  request.form['name']

    # redirect to dashboard
    return redirect('/events/dashboard')


# ! Login - POST
@app.route('/users/login', methods=['POST'])
def login():
    # get the user from db by email
    user_in_db = User.get_by_email(request.form)
    # check if the email exists
    if not user_in_db:
        flash('Email does not exist', "email")
        return redirect('/')
    # check if it matches the password in db
    if not bcrypt.check_password_hash(user_in_db.password, 
    request.form['password']):
        flash('Wrong password', "password")
        return redirect('/')
    
    # store logged in user to session
    session['user_id'] = str(user_in_db.id)
    session['name'] = user_in_db.name
    return redirect('/events/dashboard')

# ! LOG OUT
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')



#! User dashboard - liked evnets
@app.route('/users/dashboard')
def user_dashboard():
    # * check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    return redirect('/users/dashboard/events/likes')


#! User dashboard - liked events
@app.route('/users/dashboard/events/likes')
def user_dashboard_likes():
     # * check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    user = User.read_one_join_likes(data={'id': session["user_id"]})
    # pp.pprint([vars(i) for i in user.myevents])
    return render_template('user_dashboard_liked_events.html', user=user)

#! User dashboard - my events
@app.route('/users/dashboard/myevents')
def user_dashboard_my_events():
    # * check if they are logged in
    if not "user_id" in session:
        return redirect('/')
    user = User.read_one_join(data={'id': session["user_id"]})
    # pp.pprint([vars(i) for i in user.myevents])
    return render_template('user_dashboard_my_events.html', user=user)



# # ! read one - edit page
# @app.route("/users/<string:user_id>")
# def show_user(user_id):
#     if not session['logged_in']:
#         return redirect('/')

#     # print(User.read_one_join(data={'user_id': user_id}))
#     user = User.read_one_join(data={'user_id': user_id})

#     return render_template('edit.html', user=user)


# # ! update one
# @app.route('/users/update', methods=['POST'])
# def update_user():
#     # pp.pprint(request.form)
#     if not User.validate_user_update(request.form):
#         return redirect(f'/users/{session["user_id"]}')
#     data = {    
#         "first_name": request.form['first_name'],
#         "last_name": request.form['last_name'],
#         "email": request.form['email'],
#         "id": session['user_id']
#     }
#     User.update(data)
#     return redirect(f'/users/{session["user_id"]}')



