import pymongo
from pymongo import MongoClient
import os


def connect():
    client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
    return client

def insert(request):
    if not request:
        return 403
    check = request.form['Controls']
    if check == "[]":
        return 403
    else:
        contents = {
        'Start': request.form['Start'],
        'Total': request.form['TotalDistance'],
        'Controls': request.form['Controls'],
        }
        client = connect()
        mydb = client.mydb
        mydb.posts.insert_one(contents)
        client.close()
        return 200

def retreive():
    client = connect()
    if not client:
        return 500, 500, 500
    mydb = client.mydb
    body = mydb.posts.find_one(sort=[('_id', pymongo.DESCENDING)])
    print(body, flush=True)
    if not body:
        return 404, 404, 404
    Start = body['Start']
    Total = body['Total']
    Controls = body['Controls']
    client.close()
    return Start, Total, Controls