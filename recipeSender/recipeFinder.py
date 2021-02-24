import pandas as pd
import random
import math
import copy
from collections import OrderedDict


class RecipeFinder:

    def __init__(self):
        #self.recipes = pd.read_excel(r'../Oppskrifter.xlsx')
        self.recipes = pd.read_json(r'../recipeScraper/recipes.json')
        self.recipes = self.recipes.fillna(0)
        self.skipIngredients = {"vann"}

    def get_unique_recipes(self):
        dishes = self.recipes["dish"].unique()

        groupedDishes = self.recipes.groupby(by=["dish"], dropna=False).mean()

        columns = ['dish', 'url', 'veggie', 'weekend']
        uniqueDishes = pd.DataFrame(index=None, columns=columns)

        for x in dishes:
            for row, index in self.recipes.iterrows():
                if x == index.dish:
                    ingredients = []
                    for row2, index2 in self.recipes.iterrows():
                        if(index2.dish == index.dish):
                            ingredients.append(
                                {"ingredient": index2.ingredient, "amount": index2.amount, "unit": index2.unit})

                    uniqueDishes = uniqueDishes.append(
                        {
                            'dish': x,
                            'url': index.url,
                            'veggie': index.veggie,
                            'weekend': index.weekend,
                            'ingredients': ingredients,
                            'serves': index.serves,
                            'description': index.description
                        }, ignore_index=True)

                    break

        return uniqueDishes

    def pick_recipes(self, uniqueDishes, serves):
        weekRecipes = {}
        usedRecipes = []

        currentDay = 0
        weekdays = [
            "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag",
            "søndag"
        ]

        while currentDay <= 6:
            dishtype = uniqueDishes.sample()
            isWeekend = dishtype["weekend"].squeeze()
            ingredients = []
            if ((isWeekend == "no") and (currentDay <= 3) and (dishtype.dish.squeeze() not in usedRecipes)):
                weekRecipes[weekdays[currentDay]] = dishtype.to_dict('records')
                usedRecipes.append(dishtype["dish"].squeeze())
                currentDay += 1

            if ((isWeekend == "yes") and (currentDay > 3) and (dishtype.dish.squeeze() not in usedRecipes)):
                weekRecipes[weekdays[currentDay]] = dishtype.to_dict('records')
                usedRecipes.append(dishtype["dish"].squeeze())

                currentDay += 1

        weekdays = []

        for x in weekRecipes.keys():

            self.__unit_translator(
                weekRecipes[x][0]["ingredients"], weekRecipes[x][0]["serves"], serves)

            a_dictionary = {
                "day": x,
                "name": weekRecipes[x][0]["dish"],
                "link": weekRecipes[x][0]["url"],
                "ingredients": weekRecipes[x][0]["ingredients"],
                "description": weekRecipes[x][0]["description"],
                "serves": weekRecipes[x][0]["serves"]}
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
                ingredient["amount"] = math.ceil(((unitTranslationDictAmount[ingredient["unit"]] * float(
                    ingredient["amount"])) / recipeServings) * serves)
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

                if ingredient["ingredient"] in self.skipIngredients:
                    print("Skipped " + ingredient["ingredient"])
                    continue

                amountDict = {}

                ingredient["amount"],  ingredient["unit"] = self.__shoppinglist_unit_translator(
                    ingredient["unit"], ingredient["amount"])

                unitDict[ingredient["ingredient"]] = ingredient["unit"]

                if ingredient["ingredient"] in ingredientsdict:
                    ingredientsdict[ingredient["ingredient"]
                                    ] += math.ceil(ingredient["amount"])
                else:
                    ingredientsdict[ingredient["ingredient"]
                                    ] = math.ceil(ingredient["amount"])

        shoppingList = map(lambda n1:
                           {
                               "ingredient": n1,
                               "amount": ingredientsdict[n1],
                               "unit": unitDict[n1]}, ingredientsdict)

        shoppingList = self.__categorize_shopping_list(shoppingList)
        return shoppingList

    def __categorize_shopping_list(self, shoppingIngredients):

        categories = pd.read_excel("../Oppskrifter.xlsx", 'categories')
        categories["category"] = categories["category"].fillna(
            "ikke kategorisert")

        categories["basic"] = categories["basic"].fillna("no")

        basicIngredients = pd.Series(
            categories.basic.values, index=categories.ingredient).to_dict()

        categorizedShoppingList = {}
        basicShoppingList = []

        for ingredient in shoppingIngredients:
            if basicIngredients[ingredient["ingredient"]] == "yes":
                basicShoppingList.append(ingredient)
                continue

            currentCategory = categories.loc[categories['ingredient']
                                             == ingredient["ingredient"]]

            if currentCategory["category"].squeeze() in categorizedShoppingList:
                categorizedShoppingList[currentCategory["category"].squeeze()].append(
                    ingredient)

            else:
                categorizedShoppingList[currentCategory["category"].squeeze()] = [
                ]
                categorizedShoppingList[currentCategory["category"].squeeze()].append(
                    ingredient)

        return categorizedShoppingList, basicShoppingList
