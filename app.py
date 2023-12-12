"""flask app to perform operations on the movies and reviews table
     just created """
from flask import Flask, render_template, request, url_for
from datetime import datetime
from password_hashing import hash_password
from Users import login, registerUser, create_connection, create_table, create_user_recipe_table
import sqlite3 as sql
from RecipeAPI import RecipeAPI

recipe_api = RecipeAPI()

# set up the Flask object using the constructor
app = Flask(__name__)
app.static_folder = 'static'

#initialize source venv/bin/activatethe database
database = "users.db"
con = create_connection(database)
if con is not None:
    create_table(con)
    registerUser(con, "admin", "admin", "admin", 20, 1.5)
    create_user_recipe_table(con)
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
            if user[0] == 'admin':
                # Fetch user data for the admin
                cursor = con.cursor()
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                #print out all the users
                return render_template("user_page.html", username=user[0], name=user[2], users = users)
            else:
                return render_template("user_page.html", username=user[0], name=user[2], add_recipe_url= url_for('addRecipe', username=user[0]))
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


@app.route('/search', methods=['POST'])
def search_recipes():
    query = request.form['Ingredient']
    recipes = list(recipe_api.recipe_search(query))
    return render_template('search_results.html', recipes=recipes)

@app.route('/addRecipe', methods=['GET', 'POST'])
def addRecipe():
    username = request.args.get('username', None)
    if request.method == 'POST':
        handle_add_recipe_request(username)
    return render_template("add_recipe.html", username = username)

def handle_add_recipe_request(username):
    con = create_connection(database)

    try:
        recipe_name = request.form['Recipe Name']
        recipe_ingredients = request.form['Ingredients'].splitlines()
        recipe_instructions = request.form['Instructions'].splitlines()
        recipe_servings = request.form['Servings']
        recipe_calories = request.form["Calories"]
        recipe_protein = request.form["Protein"]
        recipe_fat = request.form["Fat"]
        recipe_carbs = request.form["Carbs"]

        recipe_ingredients_str = '\n'.join(recipe_ingredients)
        recipe_instructions_str = '\n'.join(recipe_instructions)

        cursor = con.cursor()
        cursor.execute("INSERT INTO user_recipes (recipe_name, username, recipe_ingredients, recipe_instructions, recipe_servings, recipe_calories, recipe_protein, recipe_fat, recipe_carbs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (recipe_name, username,  recipe_ingredients_str, recipe_instructions_str, recipe_servings, recipe_calories, recipe_protein, recipe_fat, recipe_carbs))
        con.commit()
        print(f"Recipe {recipe_name} added successfully!")
        return render_template('user_page.html', username=username, name=username)
    except Exception as e:  
        print(f"Error: {str(e)}")
        con.rollback()
        return render_template("add_recipe.html", error="An error occurred during recipe addition")
    finally:
        con.close()

if __name__ == '__main__':
    app.run(debug = True)

