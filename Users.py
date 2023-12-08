import sqlite3
from password_hashing import hash_password

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def create_table(conn):
    """Create a table for the users."""
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            username text PRIMARY KEY,
                            password text NOT NULL,
                            name text NOT NULL,
                            age integer NOT NULL,
                            height real NOT NULL
                        );""")
    except sqlite3.Error as e:
        print(e)

def create_user_recipe_table(conn):
    """Create a table for the user's recipes."""
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS user_recipes (
                            recipe_name text PRIMARY KEY,
                            username text NOT NULL,
                            recipe_ingredients text NOT NULL,
                            recipe_instructions text NOT NULL,
                            recipe_servings integer NOT NULL,
                            recipe_calories integer NOT NULL,
                            recipe_protein integer NOT NULL,
                            recipe_fat integer NOT NULL,
                            recipe_carbs integer NOT NULL,
                            FOREIGN KEY (username) REFERENCES users (username)
                        );""")
    except sqlite3.Error as e:
        print(e)

def registerUser(conn, username, password, name, age, height):
    """Register a new user."""
    hashed_password = hash_password(password)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, name, age, height) VALUES (?, ?, ?, ?, ?)",
                       (username, hashed_password, name, age, height))
        conn.commit()
        print(f"User {username} registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists. Try a different one.")

def login(conn, username, hashed_password):
    """Log in an existing user."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        if user:
            print(f"Welcome back {user[2]}!")  # user[2] is the name field
            return True, user
        else:
            print("Invalid username or password")
            return False, None
    except sqlite3.Error as e:
        print(e)
        return False, None

'''def main():
    Main function to handle user inputs.
    database = "users.db"
    conn = create_connection(database)
    if conn is not None:
        create_table(conn)

        while True:
            choice = input("Do you want to log in or register? (login/register): ").lower()
            if choice == "login":
                login(conn)
            elif choice == "register":
                register(conn)
            else:
                print("Invalid choice. Please type 'login' or 'register'.")
    else:
        print("Error! Cannot create the database connection.")'''

#if __name__ == "__main__":
   #main()"""
