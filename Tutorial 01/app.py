from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Olá mundo maravilhoso!"

@app.route('/hithere', methods=['GET'])
def hithere():
    return "Olá, eu pressionei /hithere."

@app.route('/add_two_nums', methods=['POST'])
def add_two_nums():
    body = request.get_json(force=True)

    if 'x' not in body:
        return jsonify({"error": "ERROR", "message": "Two parameters must be provided"}), 305
    elif 'y' not in body:
        return jsonify({"error": "ERROR", "message": "Two parameters must be provided"}), 305
    
    json_add = {
        "z" : body["x"] + body["y"]
    }

    return jsonify(json_add), 200

@app.route('/bye', methods=['GET'])
def bye():
    json_test = {
        'nome' : 'Orrana Lhaynher',
        'idade' : 23, 
        'telefones' : [
            {'telefone_numero' : 994675696,
             'telefone_nome' : 'Casa'
            },
            {'telefone_numero' : 994735087,
             'telefone_nome' : 'Pessoal'
            }
        ],
        'image' : [
            [0,0,0,0,1,0],
            [0,0,0,0,1,0], 
            [0,0,0,1,0,0], 
            [0,0,0,0,1,0], 
            [0,0,0,0,1,0], 
            [0,0,0,0,1,0], 
            [1,0,0,0,1,0], 
            [0,1,1,1,0,0], 
            [0,0,0,0,0,0], 
            [0,0,0,0,0,0] 
        ]
    } 

    return jsonify(json_test)

if __name__ == '__main__' :
    app.run(debug=True) #debug=True mostra erros ao rodar server