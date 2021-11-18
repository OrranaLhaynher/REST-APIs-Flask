from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.BankAPI
users = db["users"]


#####################Functions#####################

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
        return generateReturnDictionary("Invalid username", 301), True
    
    correct_password = verify(username, password)
    if not correct_password:
        return generateReturnDictionary("Invalid password", 302), True
    
    return None, False

def cashWithUser(username):
    cash = users.find({"username":username})[0]["own"]
    return cash

def debtWithUser(username):
    debt = users.find({"username":username})[0]["debt"]
    return debt

def generateReturnDictionary(message, status_code):
    result_json = {
        "message" : message,
        "status_code" : status_code
    }
    return result_json

def updateAccount(username, balance):
    users.update({"username":username},
    {
        "$set": {"own":balance}
    })

def updateDebt(username, balance):
    users.update({"username":username},
    {
        "$set": {"debt":balance}
    })


##################Resource Classes##################

class Home(Resource):
    def get(self):
        return jsonify(generateReturnDictionary("RESTful API to Handle Bank Transactions", 200))

class Register_User(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        password = body["password"]

        if userExist(username):
            return jsonify(generateReturnDictionary("Invalid username.", 301))

        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert({
            "username" : username,
            "password" : password_hashed,
            "own": 0,
            "dept": 0
        })

        return jsonify(generateReturnDictionary("Sign up performed successfully.", 200))

class Add(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        password = body["password"]
        amount = body["amount"]

        result_json, error = verifyCredentials(username, password)

        if error:
            return jsonify(result_json)

        if amount <= 0:
            return jsonify(generateReturnDictionary("Money amount entered must be greater than 0.", 304))

        cash = cashWithUser(username)

        amount-=1
        bank_cash = cashWithUser("BANK")
        updateAccount("BANK", bank_cash+1)
        updateAccount(username, amount+cash)

        return jsonify(generateReturnDictionary("Amount added sucessfully to acount.", 200))

class Transfer(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        password = body["password"]
        username_to = body["username_to"]
        amount = body["amount"]

        result_json, error = verifyCredentials(username, password)

        if error:
            return jsonify(result_json)

        cash = cashWithUser(username)
        if cash <= 0:
            return jsonify(generateReturnDictionary("You're out of money, please add or take a load.", 304))

        if not userExist(username_to):
            return jsonify(generateReturnDictionary("Invalid receiver username.", 301))

        cash_from = cashWithUser(username)
        cash_to = cashWithUser(username_to)
        bank_cash = cashWithUser("BANK")

        updateAccount("BANK", bank_cash+1)
        updateAccount(username_to, cash_to+amount-1)
        updateAccount(username, cash_from-amount)

        return jsonify(generateReturnDictionary("Amount transfered sucessfully.", 200))

class Check_Balance(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        password = body["password"]

        result_json, error = verifyCredentials(username, password)

        if error:
            return jsonify(result_json)

        result_json = users.find({"username":username},
        {
            "password":0,
            "_id":0
        })[0]

        return jsonify(result_json)

class Takeloan(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        password = body["password"]
        amount = body["amount"]

        result_json, error = verifyCredentials(username, password)

        if error:
            return jsonify(result_json)

        if amount <= 0:
            return jsonify(generateReturnDictionary("Money amount entered must be greater than 0.", 304))

        cash = cashWithUser(username)
        debt = debtWithUser(username)
        updateAccount(username, cash+amount)
        updateDebt(username, debt+amount)

        return jsonify(generateReturnDictionary("Loan added to your account.", 200))

class Payloan(Resource):
    def post(self):
        body = request.get_json()
        username = body["username"]
        password = body["password"]
        amount = body["amount"]

        result_json, error = verifyCredentials(username, password)

        if error:
            return jsonify(result_json)

        if amount <= 0:
            return jsonify(generateReturnDictionary("Money amount entered must be greater than 0.", 304))

        cash = cashWithUser(username)

        if cash < amount:
            return jsonify(generateReturnDictionary("Not enough cash in your account.", 303))

        debt = debtWithUser(username)
        updateAccount(username, cash-amount)
        updateDebt(username, debt-amount)

        return jsonify(generateReturnDictionary("You sucessfully paid your loan.", 200))


###################API Routes###################

api.add_resource(Home, '/')
api.add_resource(Register_User, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Check_Balance, '/balance')
api.add_resource(Takeloan, '/takeloan')
api.add_resource(Payloan, '/payloan')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)