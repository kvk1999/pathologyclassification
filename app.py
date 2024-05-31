from flask import Flask, render_template, request, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
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
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/chat')
def chat():
    return render_template("chat.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/buy')
def buy():
    return render_template("buy.html")

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Handle payment here (e.g., process payment using payment gateway API)
        # Redirect to a success page after successful payment
        return render_template("payment_success.html")
    else:
        return render_template("payment.html")

@app.route('/pathorepo')
def pathorepo():
    return render_template("pathorepo.html")

@app.route('/bookanappointment')
def bookanappointment():
    return render_template("bookanappointment.html")

@app.route('/forgot')
def forgot():
    return render_template("forgot.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle sign-up form submission
        # Insert new user data into the database
        return render_template("signup_success.html")
    else:
        return render_template("signup.html")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
