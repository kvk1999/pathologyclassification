from flask import Flask, request, jsonify, g, render_template, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = '123456'
DATABASE = 'ecommerce.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            dob TEXT NOT NULL,
                            username TEXT NOT NULL,
                            email TEXT NOT NULL,
                            phone_number TEXT NOT NULL,
                            password TEXT NOT NULL
                        )''')
        db.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            session['username'] = user[5]  # Assuming 5th index is username
            return jsonify({'success': True})
        else:
            return jsonify({'success': False})

    return render_template('login.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user:
            # Simulate sending email
            # In a real application, you would send an email with a reset link
            print(f'Sending password reset link to {email}')
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Email not found'})

    return render_template('forgot.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        first_name = data['firstName']
        last_name = data['lastName']
        age = data['age']
        dob = data['dob']
        username = data['username']
        email = data['email']
        phone_number = data['phoneNumber']
        password = data['password']

        db = get_db()
        cursor = db.cursor()

        # Check if username or email already exists
        cursor.execute('SELECT * FROM Users WHERE username = ? OR email = ?', (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'success': False, 'error': 'Username or email already exists'})

        cursor.execute('''
            INSERT INTO Users (first_name, last_name, age, dob, username, email, phone_number, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, age, dob, username, email, phone_number, password))
        
        db.commit()
        return jsonify({'success': True})

    return render_template('signup.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
