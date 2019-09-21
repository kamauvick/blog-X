from flask import request, render_template, url_for, redirect
from flask_login import login_user, logout_user

from app.auth import auth
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = request.form
        username = form.get('username')
        password = form.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'The user or password is not correct'
            return render_template('auth/login.html', error=error)
        is_correct_pass = user.check_password(password)
        print(is_correct_pass)
        if not is_correct_pass:
            error = 'The username or password is not correct'
            return render_template('auth/login.html', error=error)
        login_user(user)
        return url_for('/')
    return render_template('/auth/login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = request.form
        username = form.get('username')
        email = form.get('email')
        password = form.get('password')
        confirm_password = form.get('confirm_password')
        # Check for empty inputs
        if username is None and email is None and password is None and confirm_password is None:
            error = 'You cannot submit blank fields'
            return render_template('auth/signup.html', error=error)
        # Check for '' in inputs
        if ' ' in username:
            error = 'Username cannot be an empty string'
            return render_template('auth/signup.html', error=error)
        # Check if password == confirm password
        if password != confirm_password:
            error = 'The passwords do not match'
            return render_template('auth/signup.html', error=error)
        else:
            # Login the user
            user = User.query.filter_by(username=username).all()
            # Check is a username already exists
            if user is not None:
                error = 'A user with that username already exists'
                return render_template('auth/signup.html', error=error)
            user = User.query.filter_by(email=email).all()
            # Check if an email already exists
            if user is not None:
                error = 'A user with that email already exists'
                return render_template('auth/signup.html', error=error)
            # Set all fields to a user instance
            user = User(
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()
            return redirect(url_for('auth.login'))
    return render_template('auth/signup.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
