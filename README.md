-- Required Packages --
Depending on your operating system and IDE, you the following packages may not already be installed:
 - flask
 - requests
These modules must be installed in your Python environment in order to run the application.

-- To Run the Recipe & Fitness Application --
1. Run the file app.py.
2. From the console, open the web address provided in your web browser.

-- Creating a User Account --
If you don't have a user account to log into, create one.
Input your username, password, name, age, height, and daily calorie goal.
Log into your new account.

-- Adding / Editing a Recipe --
After you've created a user account and logged in, you can search for a recipe from Edamam's database or add your own recipe.
Once you've added a recipe, you can add the recipe's calories to your calorie tracker, delete the recipe, or edit the recipe.
In the ingredients and instruction fields when editing a recipe or adding your own recipe, be sure to put each seperate ingredient or instruction step on a new line.

-- Logging in as an Admin --
To log in as an administrator, use username = 'admin' and password = 'admin'.
When logged in as an administrator, you can see all of the users' information (except passwords).
You can also see each user's saved recipes, which you have the option to delete.

-- Known Bugs and Issues --
 - When adding a recipe, a user will not be able to add a recipe with the same name as an existing recipe, even if the existing recipe is saved under another user.
 - After pressing 'Save Changes' when editing a recipe, the user will be redirected to the same page, now editing a nonexistent recipe. Changes made to this recipe affect nothing, and the user is able to press 'Cancel' to return to their user page.
 - After a user's initial account creation, the user is unable to change their daily calorie goal.
 - The user's daily calorie intake cannot be reset or lowered.
 - Adding a recipe to the user's calorie intake always adds the recipe's total calories, rather than some number of servings' worth of calories.
