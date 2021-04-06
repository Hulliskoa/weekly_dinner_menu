from db import MongoDBHandler
import pandas as pd
import random
import math
import copy
import os
import sys
from collections import OrderedDict
sys.path.insert(1, '../')


class RecipeFinder:

    def __init__(self):
        self.db = MongoDBHandler()
        self.recipes = self.db.getDictFromCollection("recipes")
        self.skipIngredients = {"vann"}

    def get_unique_recipes(self):
        return self.recipes

    def pick_recipes(self, uniqueDishes, serves):
        weekRecipes = {}
        usedRecipes = []

        currentDay = 0
        weekdays = [
            "mandag", "tirsdag", "onsdag", "torsdag"  # , "fredag", "lørdag", "søndag"
        ]

        while currentDay <= 3:
            dishtype = random.choice(uniqueDishes)
            print(dishtype)
            isWeekend = dishtype["weekend"]
            ingredients = []
            if ((isWeekend == "no") and (currentDay <= 3) and (dishtype["_id"] not in usedRecipes)):
                weekRecipes[weekdays[currentDay]] = dishtype
                usedRecipes.append(dishtype["_id"])
                currentDay += 1

            if ((isWeekend == "yes") and (currentDay > 3) and (dishtype["_id"] not in usedRecipes)):
                print("Weekend")
                #weekRecipes[weekdays[currentDay]] = dishtype
                # usedRecipes.append(dishtype["_id"])
                #currentDay += 1
        weekdays = []

        for x in weekRecipes.keys():

            self.__unit_translator(
                weekRecipes[x]["ingredients"], weekRecipes[x]["serves"], serves)

            a_dictionary = {
                "day": x,
                "name": weekRecipes[x]["_id"],
                "link": weekRecipes[x]["url"],
                "ingredients": weekRecipes[x]["ingredients"],
                "description": weekRecipes[x]["description"],
                "serves": weekRecipes[x]["serves"]}
            weekdays.append(a_dictionary)
        data = []
        chosenRecipes = {"recipes": weekdays}
        data.append(chosenRecipes)
        return data

    def __unit_translator(self, ingredients, recipeServings, serves):

        unitTranslationDict = {"pound": "gram",
                               "cup": "dl"}

        unitTranslationDictAmount = {"pound": 453.59237,
                                     "cup": 2.4
                                     }
        for ingredient in ingredients:

            if ingredient["unit"] in unitTranslationDict:
                ingredient["amount"] = math.ceil(
                    ((unitTranslationDictAmount[ingredient["unit"]] * float(ingredient["amount"])) / recipeServings) * serves)
                ingredient["unit"] = unitTranslationDict[ingredient["unit"]]
            else:
                ingredient["amount"] = math.ceil((
                    (ingredient["amount"]) / recipeServings) * serves)

    def __shoppinglist_unit_translator(self, unit, amount):
        unitTranslationDict = {"pound": "gram",
                               "cup": "dl",
                               "ss": "gram",
                               "ts": "gram"}

        unitTranslationDictAmount = {"pound": 453.59237,
                                     "cup": 2.4,
                                     "ss": 15,
                                     "ts": 10
                                     }

        if unit in unitTranslationDict:
            returnAmount = unitTranslationDictAmount[unit] * float(amount)
            returnUnit = unitTranslationDict[unit]

            return math.ceil(returnAmount), returnUnit
        else:
            return math.ceil(amount), unit

    def create_shopping_list(self, currentRecipes):

        ingredientsdict = {}
        unitDict = {}
        shoppinListRecipes = copy.deepcopy(currentRecipes)

        for recipe in shoppinListRecipes[0]["recipes"]:

            for ingredient in recipe["ingredients"]:

                if ingredient["name"] in self.skipIngredients:
                    print("Skipped " + ingredient["name"])
                    continue

                amountDict = {}

                ingredient["amount"],  ingredient["unit"] = self.__shoppinglist_unit_translator(
                    ingredient["unit"], ingredient["amount"])

                unitDict[ingredient["name"]] = ingredient["unit"]

                if ingredient["name"] in ingredientsdict:
                    ingredientsdict[ingredient["name"]
                                    ] += math.ceil(ingredient["amount"])
                else:
                    ingredientsdict[ingredient["name"]] = math.ceil(
                        ingredient["amount"])

        shoppingList = map(lambda n1:
                           {
                               "ingredient": n1,
                               "amount": ingredientsdict[n1],
                               "unit": unitDict[n1]}, ingredientsdict)

        shoppingList = self.__categorize_shopping_list(shoppingList)
        return shoppingList

    def __categorize_shopping_list(self, shoppingIngredients):

        categories = self.db.returnCategoriesDF()
        categories["basic"] = categories["basic"].fillna("no")

        basicIngredients = pd.Series(
            categories.basic.values, index=categories._id).to_dict()
        categorizedShoppingList = {}
        basicShoppingList = []

        for ingredient in shoppingIngredients:
            if ingredient["ingredient"] in basicIngredients:
                if basicIngredients[ingredient["ingredient"]] == "yes":
                    basicShoppingList.append(ingredient)
                    continue

            currentCategory = categories.loc[categories['_id']
                                             == ingredient["ingredient"]]

            if len(list(currentCategory["category"])) == 0:
                categories.append(
                    {"ingredient": ingredient["ingredient"], "category": "uncategorized", "basic": "no"})
                currentCategory["category"] = ["uncategorized"]

            if currentCategory["category"].squeeze() in categorizedShoppingList:
                categorizedShoppingList[currentCategory["category"].squeeze()].append(
                    ingredient)

            else:
                categorizedShoppingList[currentCategory["category"].squeeze()] = [
                ]
                categorizedShoppingList[currentCategory["category"].squeeze()].append(
                    ingredient)
        return categorizedShoppingList, basicShoppingList
