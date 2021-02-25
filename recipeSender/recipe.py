import os
from .emailSender import EmailSender
from .recipeFinder import RecipeFinder
import sys as sys
sys.path.insert(1, '../')
import settings as settings
import db as db

class RecipeSender:

    def __init__(self):
        settings.load_settings()
        self.recipeFinder = RecipeFinder()
        self.emailSender = EmailSender()
        self.serves = 4

    def sendEmails(self):
        uniqueRecipes = self.recipeFinder.get_unique_recipes()
        weeklyRecipes = self.recipeFinder.pick_recipes(
            uniqueRecipes, self.serves)
        shoppinglist, basicShoppingList = self.recipeFinder.create_shopping_list(
            weeklyRecipes)

        print(self.emailSender.createEmail(weeklyRecipes,shoppinglist, basicShoppingList, self.serves))
