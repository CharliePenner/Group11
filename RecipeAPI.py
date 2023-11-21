
# The code within this file has been adapted from the py_edamam API found at https://github.com/JarbasAl/py_edamam/blob/master/py_edamam/__init__.py
# This file requires the requests module to be installed in your Python environment.


import requests
import json


# App ID and key for Edamam Recipe Search API
RECIPE_API_ID = "b962138b"
RECIPE_API_KEY = "7571a72dbf7b452b2f32bd26bc3efccc"

class RecipeAPI:

    def __init__(self):
        self.recipeAppId = RECIPE_API_ID
        self.recipeAppKey = RECIPE_API_KEY

    def recipe_search(self, query):
        url = 'https://api.edamam.com/search?q=' + query + '&app_id=' \
            + self.recipeAppId + '&app_key=' + self.recipeAppKey

        results = (requests.get(url)).json()

        hits = results["hits"]
        for hit in hits:
            results = hit["recipe"]
            results["yields"] = results["yield"]
            results.pop("yield")
            results["ingredient_names"] = results["ingredientLines"]
            results.pop("ingredientLines")
            results["share_url"] = results["shareAs"]
            results.pop("shareAs")
            yield Recipe(edamam=self, **results)

class Ingredient:
    def __init__(self, text=None, quantity=0, measure=None, food=None):
        self.text = text
        self.quantity = quantity
        self.measure = measure
        self.food = food

    def __repr__(self):
        return self.text

class Nutrient:
    def __init__(self, tag, label=None, quantity=0, unit=None):
        self.tag = tag
        self.label = label or tag
        self.quantity = quantity
        self.unit = unit

    def __repr__(self):
        if self.unit:
            name = "{label} * {quantity} {unit}".format(label=self.label,
                                                        quantity=self.quantity,
                                                        unit=self.unit)
        else:
            name = "{quantity} * {label}".format(label=self.label,
                                                 quanitity=self.quantity)
        return name

class Recipe:
    def __init__(self,
                 label,
                 uri="",
                 url="",
                 share_url="",
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
                 ingredient_names=None,
                 edamam=None,
                 cuisineType=None,
                 mealType=None,
                 dishType=None):
        self.ingredient_names = ingredient_names or []
        self.ingredients = []
        if isinstance(ingredients, list):
            for i in ingredients:
                ing = Ingredient(i['text'], i['quantity'], i['measure'], i['food'])
                self.ingredients.append(ing)
        else:
            self.ingredient = ingredients or []
        self.cuisineType = cuisineType or []
        self.mealType = mealType or []
        self.dishType = dishType or []
        self.label = label
        self.dietLabels = dietLabels or []
        self.healthLabels = healthLabels or []
        self.uri = uri
        self.url = url or self.uri
        self.share_url = share_url or self.url
        self.yields = yields
        self.cautions = cautions
        self.totalDaily = []
        if isinstance(totalDaily, dict):
            for n in totalDaily:
                self.totalDaily += [Nutrient(n, **totalDaily[n])]
        else:
            self.totalDaily = totalDaily or []
        self.totalWeight = totalWeight
        self.calories = calories
        self.totalTime = totalTime
        self.totalNutrients = []
        if isinstance(totalNutrients, dict):
            for n in totalNutrients:
                self.totalNutrients += [Nutrient(n, **totalNutrients[n])]
        else:
            self.totalNutrients = totalNutrients or []
        self.image = image
        if isinstance(digest, list):
            self.digest = {}
            for content in digest:
                self.digest[content["label"]] = content
        else:
            self.digest = digest or {}
        self.__edamam = edamam or Edamam()

    def __str__(self):
        return self.label

#if __name__ == "__main__":
#    e = RecipeAPI()
    
#    for recipe in e.recipe_search("Low-Carb"):
#        print("\n")
#        print(recipe)
#        print("Total calories: ", recipe.calories)
#        print(recipe.url)
#        for i in recipe.ingredients:
#            print(i)


        
