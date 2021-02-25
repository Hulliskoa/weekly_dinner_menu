
from db import MongoDBHandler
import os
import pandas as pd
import json


def updateRecipeSchema():
    recipes = pd.read_json(r'jsonDocs/recipes.json')
    # print(recipes)
    prevValue = None
    dishes = []

    dish = {}
    ingredient = {}

    for index, row in recipes.iterrows():
        if prevValue is None:
            dish = {
                "_id": row["dish"],
                "ingredients": [],
                "serves": row["serves"],
                "url": row["url"],
                "description": row["description"],
                "veggie": row["veggie"],
                "weekend": row["weekend"],
            }
        if prevValue is not None and prevValue != row["dish"]:
            dishes.append(dish)
            dish = {
                "_id": row["dish"],
                "ingredients": [],
                "serves": row["serves"],
                "url": row["url"],
                "description": row["description"],
                "veggie": row["veggie"],
                "weekend": row["weekend"],
            }

        ingredient = {
            "name": row["ingredient"],
            "amount": row["amount"],
            "unit": row["unit"]
        }
        dish["ingredients"].append(ingredient)
        prevValue = row["dish"]

def sortingCategories():
    mongoDB = MongoDBHandler()
    sorted_categories = mongoDB.returnSortedCategoriesDF()
    print(sorted_categories)
    newDF = sorted_categories.rename(columns={0: "_id"})
    newDF['order'] = 0
    newDF['order'] = newDF['order'].fillna(0)
    newDF['unicode'] = ""
    newDF['unicode'] = newDF['unicode'].fillna("")
    categories = {
            "alkohol": "1F377",
            "baking": "1F468;U+200D;U+1F373",
            "boksmat": "1F96B",
            "brus": "1F964",
            "brød": "1F35E",
            "eksotisk": "1F35C",
            "ferdigposer": "1F35C",
            "fisk": "1F41F",
            "frysedisk": "2744",
            "grønnsaker": "1F96C",
            "kjøtt": "1F969",
            "krydder": "1F9C2",
            "meieri": "1F9C0",
            "olje": "1F35C",
            "pålegg": "1F953",
            "saus": "1F372",
            "spagetti/nudler": "1F35C",
            "tilbehør": "1F35C",
            "tørrvarer": "1F960"
          }
    order = {
           "alkohol": 17,
            "baking": 16,
            "boksmat": 14,
            "brus": 18,
            "brød": 3,
            "eksotisk": 15,
            "ferdigposer": 13,
            "fisk": 2,
            "frysedisk": 6,
            "grønnsaker": 1,
            "kjøtt": 2,
            "krydder": 8,
            "meieri": 5,
            "olje": 7,
            "pålegg":  4,
            "saus": 9,
            "spagetti/nudler": 11,
            "tilbehør": 10,
            "tørrvarer": 12
           }

    for index, row in newDF.iterrows():
        if row["_id"] is not None:
            print(row["_id"])
            newDF.loc[index, "order"] = order[row["_id"]]
            newDF.loc[index, "unicode"] = categories[row["_id"]]

    mongoDB.deleteCollection("sorted-categories")
    json = newDF.to_json(orient="records")
    mongoDB.insert("sorted-categories", json)

sortingCategories()
