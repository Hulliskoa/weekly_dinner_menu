

from recipeFinder import RecipeFinder
from emailSender import EmailSender
import os
import sys

sys.path.insert(1, '../')
import settings as settings


settings.load_settings()

serves = 4

recipeFinder = RecipeFinder()
emailSender = EmailSender()

uniqueRecipes = recipeFinder.get_unique_recipes()
weeklyRecipes = recipeFinder.pick_recipes(uniqueRecipes, serves)
shoppinglist, basicShoppingList = recipeFinder.create_shopping_list(weeklyRecipes)
print(shoppinglist)
print(emailSender.createEmail(weeklyRecipes, shoppinglist, basicShoppingList, serves))



