import pymongo
from pymongo import MongoClient
import json
import pandas as pd


class MongoDBHandler:

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["weeklyRecipes"]

    def insert(self, collection, df):
        records = json.loads(df)
        col = self.db[collection]
        col.insert(records)

    def insertItem(self, collection, entity):
        try:
            col = self.db[collection]
            col.insert(json.loads(entity))
            print("Recipe stored to " + collection)
        except Exception as e:
            print("An exception occurred ::", e)

    def deleteItem(self, collection, entity):
        try:
            col = self.db[collection]
            col.delete_one({"_id": entity})
            print(entity + " deleted from " + collection)
        except Exception as e:
            print("An exception occurred ::", e)


    def deleteCollection(self, collection):
        col = self.db[collection]
        col.remove()

    def showDB(self, collection):
        col = self.db[collection]
        cursor = col.find()
        for document in cursor:
            print(document)

    def getDictFromCollection(self, collection):
        col = self.db[collection]
        array = list(col.find())
        return array

    def getItemInCollection(self, collection, item):
        col = self.db[collection]
        array = list(col.find({"_id": item}) )
        return array

    def returnDistinctIngredients(self):
        recipes = self.db["recipes"]
        return recipes.distinct("ingredients.name")

    def returnCategoriesDF(self):
        categories = self.db["categories"]
        cursor = list(categories.find())
        df = pd.DataFrame(cursor)
        return df

    def returnSortedCategoriesDF(self):
        categories = self.db["sorted-categories"]
        cursor = list(categories.find().sort("order", 1))
        df = pd.DataFrame(cursor)
        return df
