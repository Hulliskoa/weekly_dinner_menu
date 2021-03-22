import recipeSender
import recipeScraper
from db import MongoDBHandler
import os
import pandas as pd
import json
from flask import Flask
from flask import render_template
from flask.views import MethodView
from flask import request

recipeScraper = recipeScraper.RecipeScraper()
recipeSender = recipeSender.RecipeSender()

# recipeScraper.readNewEmails()
# recipeSender.sendEmails()


app = Flask(__name__)
db = MongoDBHandler()


@app.route("/")
def index():

    allRecipes = db.getDictFromCollection("recipes")
    return render_template("index.html", allrecipes=allRecipes)


class editRecipeEndpoint(MethodView):
    def get(self, entity):
        item = db.getItemInCollection("recipes", entity)
        return render_template("edit.html", item=item)

    def post(self, entity):
        data = request.data
        db.deleteItem("recipes", entity)
        db.insert("recipes", data)
        print(data)
        return "Responding to a POST request"
        """ Responds to POST requests """

    def put(self, entity):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    def patch(self, entity):
        """ Responds to PATCH requests """
        return "Responding to a PATCH request"

    def delete(self, entity):
        print(entity)
        db.deleteItem("recipes", entity)
        """ Responds to DELETE requests """
        allRecipes = db.getDictFromCollection("recipes")
        return "Responding to delete request"


app.add_url_rule("/edit/<entity>",
                 view_func=editRecipeEndpoint.as_view("edit_recipe"))


class newRecipeEndpoint(MethodView):
    def get(self, entity):
        return render_template("new.html")

    def post(self, entity):
        data = request.data
        db.insertItem("recipes", data)
        return "Responding to a POST request"

    def put(self, entity):
        return "Responding to a PUT request"

    def patch(self, entity):
        return "Responding to a PATCH request"

    def delete(self, entity):
        return "Responding to a DELETE request"


app.add_url_rule("/new/<entity>", view_func=newRecipeEndpoint.as_view("new_recipe"))


class recipeEndpoint(MethodView):
    """ Example of a class inheriting from flask.views.MethodView

    All 5 request methods are available at /api/example/<entity>
    """

    def get(self, entity):
        """ Responds to GET requests """
        print(entity)
        return "Responding to a GET request"

    def post(self, entity):
        return "Responding to a POST request"
        """ Responds to POST requests """

    def put(self, entity):
        """ Responds to PUT requests """
        return "Responding to a PUT request"

    def patch(self, entity):
        """ Responds to PATCH requests """
        return "Responding to a PATCH request"

    def delete(self, entity):
        """ Responds to DELETE requests """
        return "Responding to a DELETE request"


app.add_url_rule("/api/updaterecipe/<entity>",
                 view_func=recipeEndpoint.as_view("recipe_api"))
