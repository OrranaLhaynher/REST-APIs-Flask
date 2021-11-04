from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Olá mundo maravilhoso!"

@app.route('/hithere', methods=['GET'])
def hithere():
    return "Olá, eu pressionei /hithere."

@app.route('/bye', methods=['GET'])
def bye():
    json_test = {
        'key' : 0,
        'text' : 'Testando retorno com json.', 
        'image' : '[0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 1 0 1 0 0 0 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0]'
    }
    return jsonify(json_test)

if __name__ == '__main__' :
    app.run(debug=True) #debug=True mostra erros ao rodar server