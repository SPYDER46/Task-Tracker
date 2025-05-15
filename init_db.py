import sqlite3
import os

# Ensure the instance folder exists
os.makedirs('instance', exist_ok=True)

# Delete old database so schema changes take effect
db_path = 'instance/task_tracker.db'
if os.path.exists(db_path):
    os.remove(db_path)

# Create a fresh database connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Create tasks table with correct columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    date TEXT NOT NULL,
    project_phase TEXT NOT NULL,
    project TEXT NOT NULL,
    module TEXT NOT NULL,
    task TEXT NOT NULL,
    sub_task TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    hours REAL NOT NULL
)
''')

# Seed users only
users = [
    ('Testing Team',       'test',     '123'),
    ('FrontEnd Team',      'FrontEnd', '123'),
    ('Game Developer Team','Gamedev',  '123'),
    ('Animation Team',     'Art',      '123'),
    ('BackEnd Team',       'BackEnd',  '123')
]
for team, username, pw in users:
    cursor.execute(
        'SELECT 1 FROM users WHERE team_name=? AND username=?',
        (team, username)
    )
    if not cursor.fetchone():
        cursor.execute(
            'INSERT INTO users (team_name, username, password) VALUES (?,?,?)',
            (team, username, pw)
        )

conn.commit()
conn.close()
print("Database recreated and initialized with users only.")
