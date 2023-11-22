"""flask app to perform operations on the movies and reviews table
     just created """
from flask import Flask, render_template, request
from datetime import datetime
from password_hashing import hash_password
import sqlite3 as sql

# set up the Flask object using the constructor
app = Flask(__name__)

# Render the homepage if the user lands there
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    print("Login page accessed!")

    if request.method == 'POST':
        return handle_login_request()

    return render_template('login.html')

def handle_login_request():
    try:
        username = request.form['username']
        password = request.form['password']
        hashed_pass = hash_password(password)

        with sql.connect("users.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pass,))
            rows = cur.fetchall()

            if len(rows) == 0:
                return render_template("login.html", error="Invalid username or password")
            else:
                return render_template("index.html")
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error: {str(e)}")
        con.rollback()
        return render_template("login.html", error="An error occurred during login")
    finally:
        con.close()

@app.route('/register')
def register():
   return render_template('registerUser.html')


if __name__ == '__main__':
   app.run(debug = True)

