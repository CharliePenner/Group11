"""flask app to perform operations on the movies and reviews table
     just created """
from flask import Flask, render_template, request, url_for
from datetime import datetime
from password_hashing import hash_password
from Users import login, registerUser, create_connection, create_table, create_user_recipe_table
from Users import create_connection, create_table, create_daily_calorie_table, add_total_calories_column
import sqlite3
from RecipeAPI import RecipeAPI
from flask import Flask, request, redirect, url_for

recipe_api = RecipeAPI()

# set up the Flask object using the constructor
app = Flask(__name__)
app.static_folder = 'static'

#initialize source venv/bin/activatethe database
database = "users.db"
con = create_connection(database)
if con is not None:
    create_table(con)
    registerUser(con, "admin", "admin", "admin", 20, 1.5, 2000)
    create_user_recipe_table(con)
    create_daily_calorie_table(con)
    add_total_calories_column(con)
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
            cursor = con.cursor()

            # Fetch daily calorie goal
            cursor.execute("SELECT daily_calorie_goal FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            daily_calorie_goal = result[0] if result else None

            # Fetch total calories consumed today
            cursor.execute("SELECT SUM(total_calories) FROM daily_calories WHERE username=? AND date=date('now')", (username,))
            total_calories_result = cursor.fetchone()
            total_calories_consumed = total_calories_result[0] if total_calories_result and total_calories_result[0] is not None else 0
            
            if user[0] == 'admin':
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()

                # Fetch user recipes for the admin
                cursor.execute("SELECT * FROM user_recipes")
                user_recipes = cursor.fetchall()

                return render_template("user_page.html", username=user[0], name=user[2], users=users, user_recipes=user_recipes, daily_calorie_goal=daily_calorie_goal, total_calories_consumed=total_calories_consumed)
            else:
                # Fetch recipes for regular user
                cursor.execute("SELECT * FROM user_recipes WHERE username=?", (username,))
                user_recipes = cursor.fetchall()

                return render_template("user_page.html", username=user[0], name=user[2], add_recipe_url=url_for('addRecipe', username=user[0]), user_recipes=user_recipes, daily_calorie_goal=daily_calorie_goal, total_calories_consumed=total_calories_consumed)
        else:
            return render_template("login.html", error="Invalid username or password")
    except Exception as e:
        print(f"Error: {str(e)}")
        con.rollback()
        return render_template("login.html", error="An error occurred during login")
    finally:
        con.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return handle_register_request()
    
    return render_template('login.html')

def handle_register_request():
    con = create_connection(database)

    try:
        username = request.form['Username']
        password = request.form['Password']
        name = request.form['Name']
        age = request.form['Age']
        height = request.form['Height']
        daily_calorie_goal = request.form['DailyCalorieGoal']  # Retrieve the daily calorie goal from the form
        registerUser(con, username, password, name, age, height, daily_calorie_goal)  # Include the calorie goal in the function call
        return render_template('index.html')
    except Exception as e:  
        print(f"Error: {str(e)}")
        con.rollback()
        return render_template("login.html", error="An error occurred during registration")
    finally:
        con.close()

@app.route('/user_page/<username>')
def user_page(username):
    con = create_connection(database)
    try:
        cursor = con.cursor()

        # Query for daily calorie goal
        cursor.execute("SELECT daily_calorie_goal FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        daily_calorie_goal = result[0] if result else 2000  # Default to 2000 if not set

        # Query for total calories consumed today
        cursor.execute("SELECT SUM(total_calories) FROM daily_calories WHERE username=? AND date=date('now')", (username,))
        result = cursor.fetchone()
        total_calories_consumed = result[0] if result and result[0] is not None else 0

        # Query for user recipes
        cursor.execute("SELECT * FROM user_recipes WHERE username=?", (username,))
        user_recipes = cursor.fetchall()

        # For admin, additionally fetch all users' data
        users = []
        if username == 'admin':
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

            # Fetch all user recipes for the admin
            cursor.execute("SELECT * FROM user_recipes")
            all_user_recipes = cursor.fetchall()
            return render_template('user_page.html', username=username, daily_calorie_goal=daily_calorie_goal, total_calories_consumed=total_calories_consumed, user_recipes=user_recipes, users=users, all_user_recipes=all_user_recipes)
        
        # For regular users
        return render_template('user_page.html', username=username, daily_calorie_goal=daily_calorie_goal, total_calories_consumed=total_calories_consumed, user_recipes=user_recipes)

    except Exception as e:
        print(f"Error: {str(e)}")
        # Display an error message on the user page
        return render_template('user_page.html', username=username, error="An error occurred while fetching user data")
    finally:
        con.close()



@app.route('/delete_recipe/<username>', methods=['POST'])
def delete_recipe(username):
    con = create_connection(database)

    try:
        recipe_name = request.form['recipe_name']
        cursor = con.cursor()
        cursor.execute("DELETE FROM user_recipes WHERE username=? AND recipe_name=?", (username, recipe_name))
        con.commit()
        print(f"Recipe '{recipe_name}' deleted successfully!")
        # Redirect back to the user page after deletion
        return redirect(url_for('user_page', username=username))
    except Exception as e:
        print(f"Error: {str(e)}")
        con.rollback()
        return render_template('user_page.html', username=username, name=username, error="An error occurred during recipe deletion")
    finally:
        con.close()


@app.route('/add_recipe_to_daily_calories', methods=['POST'])
def add_recipe_to_daily_calories():
    print("Entered /add_recipe_to_daily_calories route")
    username = request.form['username']
    recipe_name = request.form['recipe_name']
    
    # Convert calories to float and then to integer
    try:
        calories = float(request.form['calories'])
        calories = int(round(calories))  # Convert to integer after rounding
    except ValueError:
        print("Invalid calorie value")
        return "Invalid calorie value", 400

    # Connect to the database
    conn = create_connection('users.db')  # Replace with your database file
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Check if there's an entry for the user for today
            cursor.execute("SELECT total_calories FROM daily_calories WHERE username = ? AND date = date('now')", (username,))
            result = cursor.fetchone()

            if result:
                # Update the existing entry
                new_total = result[0] + calories
                print(f"Updating total calories for {username} to {new_total}")
                cursor.execute("UPDATE daily_calories SET total_calories = ? WHERE username = ? AND date = date('now')", (new_total, username))
            else:
                # Create a new entry for today
                print(f"Inserting new total calories for {username}: {calories}")
                cursor.execute("INSERT INTO daily_calories (username, date, total_calories) VALUES (?, date('now'), ?)", (username, calories))

            conn.commit()
        except sqlite3.Error as e:
            print(e)
            conn.rollback()
            return "An error occurred.", 500
        finally:
            conn.close()
    else:
        return "Failed to connect to the database.", 500

    return redirect(url_for('user_page', username=username))  # Redirect back to the user page



@app.route('/search', methods=['POST'])
def search_recipes():
    query = request.form['SearchQuery']  # Get the recipe search query from the form
    username = request.form['username']  # Get the username from the form
    recipes = list(recipe_api.recipe_search(query))
    return render_template('search_results.html', recipes=recipes, username=username)

@app.route('/addRecipe', methods=['GET', 'POST'])
def addRecipe():
    username = request.args.get('username', None)
    if request.method == 'POST':
        handle_add_recipe_request(username)
    return render_template("add_recipe.html", username = username)

@app.route('/add_external_recipe/<username>', methods=['POST'])
def add_external_recipe(username):
    con = create_connection(database)

    try:
        recipe_name = request.form['Recipe Name']
        ingredients = request.form['Ingredients']
        calories = request.form['Calories']

        # Default values for other fields
        default_servings = 1
        default_protein = 0
        default_fat = 0
        default_carbs = 0
        default_instructions = "No specific instructions provided."  # Default instructions

        cursor = con.cursor()
        cursor.execute("""INSERT INTO user_recipes (recipe_name, username, recipe_ingredients, recipe_instructions, recipe_servings, recipe_calories, recipe_protein, recipe_fat, recipe_carbs)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (recipe_name, username, ingredients, default_instructions, default_servings, calories, default_protein, default_fat, default_carbs))
        con.commit()
        return redirect(url_for('user_page', username=username))
    except Exception as e:
        print(f"Error: {str(e)}")
        con.rollback()
        return redirect(url_for('user_page', username=username, error="An error occurred during recipe addition"))
    finally:
        con.close()

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

@app.route('/editRecipe', methods=['GET', 'POST'])
def editRecipe():
    username = request.args.get('username', None)
    targetName = request.args.get('targetName', None)
    targetIngredients = request.args.get('targetIngredients', None)
    targetInstructions = request.args.get('targetInstructions', None)
    targetServings = request.args.get('targetServings', None)
    targetCalories = request.args.get('targetCalories', None)
    targetProtein = request.args.get('targetProtein', None)
    targetFat = request.args.get('targetFat', None)
    targetCarbs = request.args.get('targetCarbs', None)
    if request.method == 'POST':
        handle_edit_recipe_request(username)
    return render_template("edit_recipe.html", username = username, targetName = targetName, targetIngredients = targetIngredients, targetInstructions = targetInstructions,
                            targetServings = targetServings, targetCalories = targetCalories, targetProtein = targetProtein, targetFat = targetFat, targetCarbs = targetCarbs)

def handle_edit_recipe_request(username):
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
        targetName = request.form["targetName"]

        recipe_ingredients_str = '\n'.join(recipe_ingredients)
        recipe_instructions_str = '\n'.join(recipe_instructions)

        cursor = con.cursor()
        cursor.execute("UPDATE user_recipes \
                        SET recipe_name = ?, username = ?, recipe_ingredients = ?, recipe_instructions = ?, recipe_servings = ?, \
                            recipe_calories = ?, recipe_protein = ?, recipe_fat = ?, recipe_carbs = ? \
                        WHERE recipe_name = ?",
                        (recipe_name, username,  recipe_ingredients_str, recipe_instructions_str, recipe_servings, recipe_calories, recipe_protein, recipe_fat, recipe_carbs, targetName))
        con.commit()
        print(f"Recipe {targetName} edited successfully!")
        return render_template('user_page.html', username=username, name=username)
    except Exception as e:  
        print(f"Error: {str(e)}")
        con.rollback()
        return render_template("edit_recipe.html", error="An error occurred during recipe addition")
    finally:
        con.close()

if __name__ == '__main__':
    app.run(debug = True)
