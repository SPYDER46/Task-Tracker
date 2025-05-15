import sqlite3
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, team_name, username):
        self.id = id
        self.team = team_name
        self.username = username

def get_db_connection():
    conn = sqlite3.connect('instance/task_tracker.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user(team, username, password):
    conn = get_db_connection()
    user_row = conn.execute('SELECT * FROM users WHERE team_name = ? AND username = ? AND password = ?',
                            (team, username, password)).fetchone()
    conn.close()
    if user_row:
        return User(user_row['id'], user_row['team_name'], user_row['username'])
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_row:
        return User(user_row['id'], user_row['team_name'], user_row['username'])
    return None

def get_tasks(team):
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks WHERE team_name = ?', (team,)).fetchall()
    conn.close()
    return tasks

def add_task(task_data):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO tasks (team_name, date, project_phase,  project, module, task, sub_task, assigned_to, hours)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', task_data)
    conn.commit()
    conn.close()

def delete_task(task_id, team):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ? AND team_name = ?', (task_id, team))
    conn.commit()
    conn.close()