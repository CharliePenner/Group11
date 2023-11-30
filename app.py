"""flask app to perform operations on the movies and reviews table
     just created """
from flask import Flask, render_template, request
from datetime import datetime
from password_hashing import hash_password
from Users import login, registerUser, create_connection, create_table
import sqlite3 as sql

# set up the Flask object using the constructor
app = Flask(__name__)

#initialize the database
database = "users.db"
con = create_connection(database)
if con is not None:
    create_table(con)
    registerUser(con, "admin", "admin", "admin", 20, 1.5)
con.close()

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
    con = create_connection(database)

    try:
        username = request.form['Username']
        password = request.form['Password']
        hashed_pass = hash_password(password)
        success, user = login(con, username, hashed_pass)

        if success:
            return render_template("user_page.html", username=user[0], name=user[2])  # Customize as needed
        else:
            return render_template("login.html", error="Invalid username or password")
              
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error: {str(e)}")
        con.rollback()
        return render_template("login.html", error="An error occurred during login")
    finally:
        con.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return handle_register_request()
    
    return render_template('registerUser.html')

def handle_register_request():
    con = create_connection(database)

    try:
        username = request.form['Username']
        password = request.form['Password']
        name = request.form['Name']
        age = request.form['Age']
        height = request.form['Height']
        registerUser(con, username, password, name, age, height)
        return render_template('index.html')
    except Exception as e:  
        print(f"Error: {str(e)}")
        con.rollback()
        return render_template("registerUser.html", error="An error occurred during registration")
    finally:
        con.close()

if __name__ == '__main__':
    app.run(debug = True)


