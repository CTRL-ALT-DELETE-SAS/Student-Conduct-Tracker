from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user
from App.controllers import User
from flask_jwt import JWT

from App.controllers.auth import (
    authenticate,
)

app = Flask('auth_views', __name__, template_folder='../templates')
app.secret_key = '6ZN40RI0iq'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#Define route for Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']

        user = authenticate(firstname, lastname, password)

        if user:
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your name and password.', 'danger')

    return render_template('login.html')

# Define route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

