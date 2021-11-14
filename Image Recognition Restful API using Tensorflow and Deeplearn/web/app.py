from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests
import tensorflow
import json
import subprocess

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageRecognition
users = db["users"]


########## Functions ##########

def userExist(username):
    if users.find({"username":username}).count() == 0:
        return False
    else:
        return True

def verify(username, password):
    if not userExist(username):
        return False

    user_psw_hashed = users.find({"username" : username})[0]["password"]

    if bcrypt.hashpw(password.encode('utf-8'), user_psw_hashed) == user_psw_hashed:
        return True
    else:
        return False

def verifyCredentials(username, password):
    if not userExist(username):
        return generateReturnDictionary("Invalid user", 301), True
    
    correct_password = verify(username, password)
    if not correct_password:
        return generateReturnDictionary("Invalid password", 302), True
    
    return None, False

def countTokens(username):
    user_tokens = users.find({
        "username" : username
    })[0]["tokens"]
    return user_tokens

def generateReturnDictionary(message, status_code):
    result_json = {
        "message" : message,
        "status_code" : status_code
    }
    return result_json


########## Resource Classes ##########

class Home(Resource):
    def get(self):
        result_json = {
            "message" : "Image Recognition RESTful API using Tensorflow and Deeplearn",
            "status_code" : 200
        }

        return jsonify(result_json)

class Register_Users(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        password = body["password"]

        if userExist(username):
            result_json = {
                "message" : "Invalid username",
                "status_code" : 301
            }
            return jsonify(result_json)

        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert({
            "username" : username,
            "password" : password_hashed,
            "tokens" : 4
        })

        result_json = {
            "message" : "Sign up performed successfully",
            "status_code" : 200
        }

        return jsonify(result_json)

class Classify_Image(Resource):
    def post(self):
        body = request.get_json()
        username = body['username']
        password = body['password']
        url = body['url']

        res_json, error = verifyCredentials(username, password)

        if error:
            return jsonify(res_json)

        num_tokens = countTokens(username)

        if num_tokens <= 0:
            return jsonify(generateReturnDictionary("Not enough tokens!", 303))

        r = requests.get(url)
        result_json = {}

        with open("temp.jpg", "wb") as f:
            f.write(r.content)
            proc = subprocess.Popen('python classiy_image.py --model_dir=. --image_file=./temp.jpg')
            proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                result_json = json.load(g)

        users.update({
            "username" : username
        },
        {
            "$set" : { 
                "tokens" : num_tokens - 1
            }
        })

        return result_json

class Refill_Tokens(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        admin_password = body["admin_password"]
        refill_amount = body["refill"]

        if not userExist(username):
            return jsonify(generateReturnDictionary("Invalid username", 301))

        correct_pw = "abc123"
        if not admin_password == correct_pw:
            return jsonify(generateReturnDictionary("Invalid admin password", 304))

        users.update({
            "username" : username
        },
        {
            "$set" : { 
                "tokens" : refill_amount 
            }
        })

        return jsonify(generateReturnDictionary(str("Refilled tokens successfully. Your new number of tokens is "+str(refill_amount)), 200))

########## API Routes ##########

api.add_resource(Home, '/')
api.add_resource(Register_Users, '/register')
api.add_resource(Classify_Image, '/classify')
api.add_resource(Refill_Tokens, '/refill')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)