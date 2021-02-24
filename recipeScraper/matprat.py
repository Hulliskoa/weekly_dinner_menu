from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import load_workbook
import re
class MatpratScraper:
    def __init__(self):
        self.service = Service('chromedriver.exe')
        self.service.start()
        chrome_options = Options()
        chrome_options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)


    def scrape(self, urlToScrape):

        xlsRecipes = pd.read_excel(r'../Oppskrifter.xlsx')
        xlsRecipes.to_json(r'¨../jsonDocs/xlsrecipes.json')

        scrapedRecipes = pd.read_json(r'../jsonDocs/scrapedRecipes.json')

        columns = {"dish", "amount", "unit", "ingredient",
                   "serves", "url", "weekend", "veggie", "description"}

        recipeDf = pd.DataFrame(columns=columns)

        self.driver.get(urlToScrape)
        ingredientRow = {}

        dish = self.driver.find_element_by_xpath(
            '/html/body/form/div[3]/div/div[2]/div/section/div[1]/header/h1')
        servers = self.driver.find_element_by_xpath(
            '/html/body/form/div[3]/div/div[2]/div/section/div[2]/div[1]/div/fieldset/div/input')
        servers = servers.get_attribute("value")
        typeDish = self.driver.find_element_by_xpath(
            '/html/body/form/div[3]/div/div[2]/div/section/div[1]/header/dl/dd[1]')
        typeDish = typeDish.text
        description = self.driver.find_element_by_xpath(
            '/html/body/form/div[3]/div/div[2]/div/section/div[1]/div[2]/p')
        description = description.text

        containers = self.driver.find_elements_by_class_name('ingredientsList')

        for elements in containers:
            items = elements.find_elements_by_tag_name("li")

            for listItem in items:

                amountItem = listItem.find_element_by_class_name('amount')
                unitItem = listItem.find_element_by_class_name('unit')
                ingredientRow["dish"] = dish.text
                ingredient = listItem.text

                ingredientRow["amount"] = amountItem.text
                ingredientRow["unit"] = unitItem.text
                ingredient = ingredient.replace(ingredientRow["amount"], "")
                ingredientRow["ingredient"] = ingredient.replace(
                    ingredientRow["unit"], "")
                ingredientRow["ingredient"] = ingredientRow["ingredient"].strip()
                ingredientRow["ingredient"] = re.sub(' +', ' ', ingredientRow["ingredient"])
                ingredientRow["amount"] = float(
                    ingredientRow["amount"].replace(",", ".", 1))

                ingredientRow["serves"] = servers
                ingredientRow["url"] = urlToScrape

                if typeDish != "gjester":
                    ingredientRow["weekend"] = "no"
                else:
                    ingredientRow["weekend"] = "yes"

                if typeDish != "vegetar":
                    ingredientRow["veggie"] = "no"
                else:
                    ingredientRow["veggie"] = "yes"

                ingredientRow["description"] = re.sub(' +', ' ', description)
                recipeDf = recipeDf.append(ingredientRow, ignore_index=True)


        if recipeDf["dish"][0] not in scrapedRecipes["dish"].values:
            scrapedRecipes = scrapedRecipes.append(recipeDf, ignore_index=True)
            scrapedRecipes.to_json(r'../jsonDocs/scrapedRecipes.json')
            recipes = scrapedRecipes.append(xlsRecipes, ignore_index=True)
            recipes.to_json(r'../jsonDocs/recipes.json')
            print("added new recipe")

        self.driver.close()


