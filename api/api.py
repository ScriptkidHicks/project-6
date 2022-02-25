"""
Brevets RESTful API
"""
from flask import Flask
import os
from flask_restful import Api
from mongoengine import connect
from resources import BrevetsAPI
from resources import BrevetAPI

API_PORT = os.environ.get('API_PORT')


app = Flask(__name__)
api = Api(app)
connect("Brevets", host="db", port=27017)

api.add_resource(BrevetAPI, "/api/Brevet/<id>")
api.add_resource(BrevetsAPI, "/api/Brevets")


if __name__ == "__main__":
    print("Opening api for global access on port {}".format(API_PORT))
    app.run(port=API_PORT, host="0.0.0.0")