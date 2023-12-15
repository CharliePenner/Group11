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
    """Create a table for the users, including the daily calorie goal."""
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            username TEXT PRIMARY KEY,
                            password TEXT NOT NULL,
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            height REAL NOT NULL,
                            daily_calorie_goal INTEGER DEFAULT 2000
                        );""")
    except sqlite3.Error as e:
        print(e)

def create_user_recipe_table(conn):
    """Create a table for the user's recipes."""
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS user_recipes (
                            recipe_name TEXT PRIMARY KEY,
                            username TEXT NOT NULL,
                            recipe_ingredients TEXT NOT NULL,
                            recipe_instructions TEXT NOT NULL,
                            recipe_servings INTEGER NOT NULL,
                            recipe_calories INTEGER NOT NULL,
                            recipe_protein INTEGER NOT NULL,
                            recipe_fat INTEGER NOT NULL,
                            recipe_carbs INTEGER NOT NULL,
                            FOREIGN KEY (username) REFERENCES users (username)
                        );""")
    except sqlite3.Error as e:
        print(e)

def create_daily_calorie_table(conn):
    """Create a table for tracking daily calorie intake."""
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS daily_calories (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            date TEXT NOT NULL,
                            recipe_calories INTEGER DEFAULT 0,
                            FOREIGN KEY (username) REFERENCES users (username)
                        );""")
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def add_total_calories_column(conn):
    """Add the total_calories column to the daily_calories table."""
    try:
        cursor = conn.cursor()
        cursor.execute("""ALTER TABLE daily_calories ADD COLUMN total_calories INTEGER DEFAULT 0""")
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def registerUser(conn, username, password, name, age, height, daily_calorie_goal):
    """Register a new user, including setting their daily calorie goal."""
    hashed_password = hash_password(password)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, name, age, height, daily_calorie_goal) VALUES (?, ?, ?, ?, ?, ?)",
                       (username, hashed_password, name, age, height, daily_calorie_goal))
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
