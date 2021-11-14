from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]


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

def countTokens(username):
    user_tokens = users.find({
        "username" : username
    })[0]["tokens"]
    return user_tokens


########## Resource Classes ##########

class Home(Resource):
    def get(self):
        result_json = {
            "message" : "RESTful API for Similarity Check Using NLP",
            "status_code" : 200
        }

        return jsonify(result_json)

class Register_User(Resource):
    def post(self):
        body = request.get_json()
        username = body['username']
        password = body['password']

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
            "tokens" : 10
        })

        result_json = {
            "message" : "Sign up performed successfully",
            "status_code" : 200
        }

        return jsonify(result_json)

class Detect_Similarity(Resource):
    def post(self):
        body = request.get_json()
        username = body['username']
        password = body['password']
        text_one = body['text_1']
        text_two = body['text_2']

        if not userExist(username):
            result_json = {
                "message" : "Invalid username",
                "status_code" : 301
            }
            return jsonify(result_json)

        correct_user = verify(username, password)

        if not correct_user:
            result_json = {
                "message" : "Invalid password",
                "status_code" : 302
            }
            return jsonify(result_json)

        num_tokens = countTokens(username)

        if num_tokens <= 0:
            result_json = {
                "message" : "User out of tokens, please refill!!!",
                "status_code" : 303
            }
            return jsonify(result_json)

        nlp = spacy.load('pt_core_news_sm')

        text_one = nlp(text_one)
        text_two = nlp(text_two)

        ratio = text_one.similarity(text_two)

        result_json = {
            "message" : "Similarity score calculated successfully.",
            "similarity" : ratio,
            "status_code" : 200
        }

        users.update({
            "username" : username
        },
        {
            "$set" : { 
                "tokens" : num_tokens - 1
            }
        })

        return jsonify(result_json)

class Refill(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        admin_password = body["admin_password"]
        refill_amount = body["refill"]

        if not userExist(username):
            result_json = {
                "message" : "Invalid username",
                "status_code" : 301
            }
            return jsonify(result_json)

        correct_pw = "abc123"

        if not admin_password == correct_pw:
            result_json = {
                "message" : "Invalid admin password",
                "status_code" : 304
            }
            return jsonify(result_json)

        num_tokens = countTokens(username)

        users.update({
            "username" : username
        },
        {
            "$set" : { 
                "tokens" : refill_amount
            }
        })

        result_json = {
            "message" : "Refilled tokens successfully.",
            "num_tokens": refill_amount,
            "status_code" : 200
        }
        return jsonify(result_json)


########## API Routes ##########

api.add_resource(Home, '/')
api.add_resource(Register_User, '/register')
api.add_resource(Detect_Similarity, '/detect')
api.add_resource(Refill, '/refill')


if __name__ == '__main__' :
    app.run(host="0.0.0.0", port=5000)