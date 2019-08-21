from flask import Flask
from flask import request
from flask.json import jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson import json_util
import json

# to connect local mongo db
client = MongoClient('localhost:27017')
db = client.ContactDB

app = Flask(__name__)

'''
function to add contact

'''
@app.route("/add_contact", methods = ['POST'])
def add_contact():
    try:
        data = json.loads(request.data)
        user_name = data['name']
        user_contact = data['contact']
        if user_name and user_contact:
            status = db.Contacts.insert_one({
                "name" : user_name,
                "contact" : user_contact
            })
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})
    

'''
function to get all contacts

'''
@app.route("/get_all_contact", methods = ['GET'])
def get_all_contact():
    try:
        contacts = db.Contacts.find()
        return dumps(contacts)
    except Exception as e:
        return dumps({'error' : str(e)})
    

'''
function to update_contact

'''
@app.route("/update_contact", methods = ['POST'])
def update_contact():
    try:
        data = json.loads(request.data)
        user_name = data['name']
        user_contact = data['contact']
        contacts = db.Contacts.find_one(
            {"name": user_name})
        if contacts:
            status = db.Contacts.update_one({
                "name" : user_name
            },
             {'$set': { "name" : user_name, "contact": user_contact }})
        
            return dumps({'message' : 'SUCCESS'})
        else:
            return dumps({'message' : 'userName does not exists'})
    except Exception as e:
        return dumps({'error' : str(e)})

'''
function to delete_contact

'''
@app.route("/delete_contact", methods = ['POST'])
def delete_contact():
    try:
        data = json.loads(request.data)
        user_name = data['name']
        if user_name:
            value = db.Contacts.delete_one({
                "name" : user_name
            })
        return dumps(value)
    except Exception as e:
        return dumps({'error' : str(e)})
    
'''
function to get particular contact

'''    
@app.route("/get_contact/<name>", methods = ['GET'])
def get_contact(name):
    try:
        user_name = name
        contacts = db.Contacts.find_one(
            {"name": user_name})
        return dumps(contacts)
#       return json_util.dumps({'cursor': contacts})
#       return dumps(contacts)
    except Exception as e:
        return dumps({'error' : str(e)})
    
if __name__ == '__main__':
    app.run(debug=True)
