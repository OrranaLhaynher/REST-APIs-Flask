from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def checkPostedData(postedData, functionName):
    if functionName == 'add' or functionName == 'substract' or functionName == 'multiply':
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

class Add(Resource):
    def post(self):
        body = request.get_json()

        status_code = checkPostedData(body, "add")
        if (status_code != 200):
            json_add = {
                "message" : "An error occurred.",
                "status" : status_code
            }
            return json_add

        json_add = {
            "message" : int(body['x']) + int(body['y']),
            "status" : 200
        }

        return jsonify(json_add)

class Subtract(Resource):
    def post(self):
        body = request.get_json()

        status_code = checkPostedData(body, "subtract")
        if (status_code != 200):
            json_add = {
                "message" : "An error occurred.",
                "status" : status_code
            }
            return json_add

        json_add = {
            "message" : int(body['x']) - int(body['y']),
            "status" : 200
        }

        return jsonify(json_add)

class Multiply(Resource):
    def post(self):
        body = request.get_json()

        status_code = checkPostedData(body, "multiply")
        if (status_code != 200):
            json_add = {
                "message" : "An error occurred.",
                "status" : status_code
            }
            return json_add

        json_add = {
            "message" : int(body['x']) * int(body['y']),
            "status" : 200
        }

        return jsonify(json_add)

class Divide(Resource):
    def post(self):
        body = request.get_json()

        status_code = checkPostedData(body, "divide")
        if (status_code != 200):
            json_add = {
                "message" : "An error occurred.",
                "status" : status_code
            }
            return json_add

        json_add = {
            "message" : int(body['x']) / int(body['y']),
            "status" : 200
        }

        return jsonify(json_add)

api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')

if __name__ == '__main__' :
    app.run(debug=True)