
# The code within this file has been adapted from the py_edamam API found at https://github.com/JarbasAl/py_edamam/blob/master/py_edamam/__init__.py
# This file requires the requests module to be installed in your Python environment.


import requests
import json


# App ID and key for Edamam Recipe Search API
RECIPE_API_ID = "b962138b"
RECIPE_API_KEY = "7571a72dbf7b452b2f32bd26bc3efccc"

def filter_recipe_keys(data, allowed_keys):
    return {k: v for k, v in data.items() if k in allowed_keys}

# class for using the Edamam Recipe Search API
class RecipeAPI:
    def __init__(self):
        self.recipeAppId = RECIPE_API_ID
        self.recipeAppKey = RECIPE_API_KEY

    def recipe_search(self, query):
        url = 'https://api.edamam.com/search?q=' + query + '&app_id=' \
            + self.recipeAppId + '&app_key=' + self.recipeAppKey

        # retrieves search results and converts from json
        results = (requests.get(url)).json()

        # search results are stored as a dict
        hits = results["hits"]

        # Define allowed keys based on your Recipe class constructor
        allowed_keys = ['label', 'uri', 'url', 'shareAs', 'image',
                        'dietLabels', 'healthLabels', 'yields', 'cautions',
                        'totalDaily', 'totalWeight', 'calories', 'totalTime',
                        'totalNutrients', 'digest', 'ingredients',
                        'source', 'ingredientLines', 'cuisineType', 
                        'mealType', 'dishType']

        for hit in hits:
            recipe_data = hit["recipe"]
            recipe_data["yields"] = recipe_data["yield"]
            recipe_data.pop("yield")
            recipe_data["calories"] = round(recipe_data["calories"])
            filtered_data = filter_recipe_keys(recipe_data, allowed_keys)
            yield Recipe(**filtered_data)

# class for storing an individual ingredient found within a recipe, with all the attributes Edamam provides
class Ingredient:
    def __init__(self,
                 text=None,
                 quantity=0,
                 measure=None,
                 food=None,
                 weight=0,
                 foodCategory=None,
                 foodId=None,
                 image=None):
        self.text = text
        self.quantity = quantity
        self.measure = measure
        self.food = food
        self.weight = weight
        self.foodCategory = foodCategory
        self.foodId = foodId
        self.image = image

    def __repr__(self):
        return self.text

# class for storing an individual nutrient found within a recipe, with all the attributes Edamam provides
class Nutrient:
    def __init__(self, tag, label=None, quantity=0, unit=None):
        self.tag = tag
        self.label = label or tag
        self.quantity = quantity
        self.unit = unit

    def __repr__(self):
        if self.unit:
            name = "{label}: {quantity} {unit}".format(label=self.label,
                                                        quantity=self.quantity,
                                                        unit=self.unit)
        else:
            name = "{label}: {quantity}".format(label=self.label,
                                                 quanitity=self.quantity)
        return name

# class for storing an individual recipe, with all the attributes Edamam provides
class Recipe:
    def __init__(self,
                 label,
                 uri="",
                 url="",
                 shareAs="",
                 image=None,
                 dietLabels=None,
                 healthLabels=None,
                 yields=1.0,
                 cautions=None,
                 totalDaily=None,
                 totalWeight=0,
                 calories=0,
                 totalTime=0,
                 totalNutrients=None,
                 digest=None,
                 ingredients=None,
                 source="edamam",
                 ingredientLines=None,
                 cuisineType=None,
                 mealType=None,
                 dishType=None):
        self.ingredientLines = ingredientLines or []        # simple ingredient text
        self.ingredients = []                               # complex ingredient object
        if isinstance(ingredients, list):
            for i in ingredients:                           # copies list of ingredient dicts to list of Ingredient objects
                ing = Ingredient(**i)
                self.ingredients.append(ing)
        else:
            self.ingredient = ingredients or []
        self.cuisineType = cuisineType or []                # dish regional origin or inspiration
        self.mealType = mealType or []                      # breakfast/lunch/dinner
        self.dishType = dishType or []                      # main course/starter/etc.
        self.label = label                                  # recipe title
        self.dietLabels = dietLabels or []                  # diets that fit this recipe
        self.healthLabels = healthLabels or []              # dietary restrictions satisfied by recipe (e.g. "Peanut-Free")
        self.uri = uri
        self.url = url or self.uri                          # url to original recipe
        self.shareAs = shareAs or self.url                  # url to recipe on Edamam
        self.yields = yields                                # number of servings
        self.cautions = cautions                            # hidden allergen warnings
        self.totalDaily = []
        if isinstance(totalDaily, dict):
            for n in totalDaily:                            # copies nutrient daily values to list of Nutrient objects
                nut = Nutrient(n, **totalDaily[n])
                self.totalDaily.append(nut)
        else:
            self.totalDaily = totalDaily or []
        self.totalWeight = totalWeight
        self.calories = calories
        self.totalTime = totalTime
        self.totalNutrients = []
        if isinstance(totalNutrients, dict):
            for n in totalNutrients:                        # copies nutrient total amounts to list of Nutrient objects
                nut = Nutrient(n, **totalNutrients[n])
                self.totalNutrients.append(nut)
        else:
            self.totalNutrients = totalNutrients or []
        self.image = image
        if isinstance(digest, list):
            self.digest = {}
            for content in digest:
                self.digest[content["label"]] = content
        else:
            self.digest = digest or {}

    def __str__(self):
        return self.label

#TESTING
if __name__ == "__main__":
    e = RecipeAPI()
    query = input("Recipe Search: ")
    for recipe in e.recipe_search(query):
        print("\n")
        print(recipe)
        print("Total calories: ", recipe.calories)
        print(recipe.url)
        print("Ingredients:")
        for i in recipe.ingredients:
            print("\t", i)
        print("Nutrients (Total):")
        for n in recipe.totalNutrients:
            print("\t", n)
