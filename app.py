from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuration for SQLite database
DATABASE = 'users.db'

# Function to create the database table if it doesn't exist
def create_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )''')
        conn.commit()

# Function to insert a new user into the database
def insert_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()

# Function to retrieve a user from the database by username
def get_user(username):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = get_user(username)
    if user and user[2] == password:
        return f'Hello, {username}! You are logged in.'
    else:
        return 'Invalid username or password. Please try again.'
if __name__ == '__main__':
    # create_table() 
    # insert_user('admin', 'admin123') # Create the users table in the database
    app.run(debug=True)
