from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from .models import get_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))

    if request.method == 'POST':
        team = request.form['team_name']
        username = request.form['username']
        password = request.form['password']

        user = get_user(team, username, password)
        if user:
            login_user(user)
            return redirect(url_for('main.homepage'))
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))