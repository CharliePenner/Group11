import sqlite3
import hashlib

#connect to db, creates one if it doesn't exits
conn = sqlite3.connect('accounts.db')
cursor = conn.cursor()
#create users table
conn.execute('CREATE TABLE USERS (Username TEXT, Password TEXT, Current_Weight INT, Curr_Height INT)')


def create_user(user, password, weight, height ):
    hashed_pass = hashlib.sha256(password.encode()).hexdigest()
    #insert try except finally
    cursor.execute('INSERT INTO USERS (Username, Password, Current_Weight, Current_Height) VALUES (?, ?, ?, ?)', (user, hashed_pass, weight, height))
    conn.commit()
    conn.close()
