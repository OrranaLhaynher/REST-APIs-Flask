from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

def checkPostedData(postedData, functionName):
    if functionName == 'add' or functionName == 'subtract' or functionName == 'multiply':
        if 'x' not in postedData or 'y' not in postedData:
            return 400
        else:
            return 200
    elif functionName == 'divide':
        if 'x' not in postedData or 'y' not in postedData:
            return 400
        elif int(postedData['y']) == 0:
            return 302
        else:
            return 200
    else:
        print('Nome de resource errado.')

    return postedData

def verify(username, password):
    user_psw_hashed = users.find({"username" : username})[0]["password"]

    if bcrypt.hashpw(password.encode('utf-8'), user_psw_hashed) == user_psw_hashed:
        return True
    else:
        return False

def countTokens(username):
    user_tokens = users.find({"username" : username})[0]["tokens"]
    return user_tokens
 

class Register_User(Resource):
    def post(self):
        body = request.get_json()

        username = body["username"]
        password = body["password"]

        #hash(password + salt) 
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        #store username and password into database
        users.insert({
            "username" : username,
            "password" : password_hashed,
            "sentence" : "",
            "tokens" : 10
        })

        result_json = {
            "message" : "Sign up performed successfully",
            "status_code" : 200
        }

        return jsonify(result_json)


class Store_Sentence(Resource):
    def post(self):
        body = request.get_json()

        username = body["username"]
        password = body["password"]
        sentence = body["sentence"]

        correct_user = verify(username, password)

        if not correct_user:
            result_json = {
                "message" : "User not registered in system",
                "status_code" : 302
            }
            return jsonify(result_json)

        num_tokens = countTokens(username)

        if num_tokens <= 0:
            result_json = {
                "message" : "User out of tokens",
                "status_code" : 301
            }
            return jsonify(result_json)

        users.update({
            "username" : username
        },
        {
            "$set" : {
                "sentence" : sentence, 
                "tokens" : num_tokens - 1
            }
        })

        result_json = {
            "message" : "Sentence stored successfully",
            "status_code" : 200
        }

        return jsonify(result_json)

class Retrieve_Sentence(Resource):
    def post(self):
        body = request.get_json()

        username = body["username"]
        password = body["password"]
        
        correct_user = verify(username, password)

        if not correct_user:
            result_json = {
                "message" : "User not registered in system",
                "status_code" : 302
            }
            return jsonify(result_json)

        num_tokens = countTokens(username)

        if num_tokens <= 0:
            result_json = {
                "message" : "User out of tokens",
                "status_code" : 301
            }
            return jsonify(result_json)

        users.update({
            "username" : username
        },
        {
            "$set" : {
                "tokens" : num_tokens - 1
            }
        })

        sentences = users.find({
                        "username" : username
                    })[0]["sentence"]

        result_json = {
            "message" : sentences,
            "status_code" : 200
        }

        return jsonify(result_json)


#API routes
api.add_resource(Register_User, '/register')
api.add_resource(Store_Sentence, '/store')
api.add_resource(Retrieve_Sentence, '/retrieve')

if __name__ == '__main__' :
    app.run(host="0.0.0.0", port=5000)