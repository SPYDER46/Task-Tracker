from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import (
    login_user, current_user, login_required,
    LoginManager, UserMixin, logout_user
)
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('instance/task_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, id, team_name, username, password):
        self.id = id
        self.team = team_name
        self.username = username
        self.password = password

    @staticmethod
    def from_row(row):
        return User(row['id'], row['team_name'], row['username'], row['password']) if row else None

# Authentication helpers
def get_user(team_name, username, password):
    conn = get_db_connection()
    row = conn.execute(
        'SELECT * FROM users WHERE team_name = ? AND username = ? AND password = ?',
        (team_name, username, password)
    ).fetchone()
    conn.close()
    return User.from_row(row)

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return User.from_row(row)

# Task helpers
def get_tasks_for_team(team_name):
    conn = get_db_connection()
    tasks = conn.execute(
        'SELECT * FROM tasks WHERE team_name = ?', (team_name,)
    ).fetchall()
    conn.close()
    return tasks

# Routes

@app.route('/team_homepage')
@login_required
def team_homepage():
    all_tasks = get_tasks_for_team(current_user.team)
    # Get filters
    filter_date = request.args.get('filter_date')
    search = request.args.get('search', '').lower()

    # Apply date filter
    if filter_date:
        all_tasks = [t for t in all_tasks if t['date'] == filter_date]

    # Apply search filter
    if search:
        def matches(task):
            return (search in task['project_phase'].lower() or
                    search in task['project'].lower() or
                    search in task['task'].lower() or
                    search in task['assigned_to'].lower())
        all_tasks = [t for t in all_tasks if matches(t)]

    return render_template('index.html', tasks=all_tasks)

@app.route('/add', methods=['POST'])
@login_required
def add():
    data = (
        current_user.team,
        request.form['date'],
        request.form['project_phase'],
        request.form['project'],
        request.form['module'],
        request.form['task'],
        request.form['sub_task'],
        request.form['assigned_to'],
        float(request.form['hours'])
    )
    conn = get_db_connection()
    conn.execute(
        '''
        INSERT INTO tasks
          (team_name, date, project_phase, project, module, task, sub_task, assigned_to, hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        data
    )
    conn.commit()
    conn.close()

    # flash('Task added successfully!', 'success')
    return redirect(url_for('team_homepage'))

@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute(
        'DELETE FROM tasks WHERE id = ? AND team_name = ?',
        (task_id, current_user.team)
    )
    conn.commit()
    conn.close()

    # flash('Task deleted successfully!', 'success')
    return redirect(url_for('team_homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('team_homepage'))

    if request.method == 'POST':
        team_name = request.form.get('team_name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = get_user(team_name, username, password)
        if user:
            login_user(user)
            return redirect(url_for('team_homepage'))
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
