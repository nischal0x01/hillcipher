from flask import Flask, request, jsonify
from flask_cors import CORS
from hill_cipher import HillCipher

app = Flask(__name__)
CORS(app)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    hill = HillCipher(data['key_matrix'])
    result = hill.encrypt(data['plaintext'])
    return jsonify({'result': result})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    hill = HillCipher(data['key_matrix'])
    result = hill.decrypt(data['ciphertext'])
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)