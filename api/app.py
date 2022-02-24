"""
Brevets RESTful API
"""

from flask import Flask
import os
from flask_restful import Resource, Api

BREVETS_PORT = os.environ.get('BREVETS_PORT')


app = Flask(__name__)
api = Api(app)


if __name__ == "__main__":
    print("Opening api for global access on port {}".format(BREVETS_PORT))
    app.run(port=BREVETS_PORT, host="0.0.0.0")