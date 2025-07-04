from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from hillcipher import HillCipher
import random, os

app = Flask(__name__, static_folder="../frontend")
CORS(app)

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api/encrypt", methods=["POST"])
def encrypt():
    data = request.json
    try:
        cipher = HillCipher(data['key_matrix'])
        plaintext = data['plaintext']
        if not any(c.isalpha() for c in plaintext):
            raise ValueError("Plaintext must contain alphabetic characters (A-Z) only.")
        result = cipher.encrypt(plaintext)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/decrypt", methods=["POST"])
def decrypt():
    data = request.json
    try:
        cipher = HillCipher(data['key_matrix'])
        result = cipher.decrypt(data['ciphertext'])
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/api/validate", methods=["POST"])
def validate():
    try:
        HillCipher(request.json['key_matrix'])
        return jsonify({'valid': True})
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)})

@app.route("/api/generate-key", methods=["POST"])
def generate_key():
    size = request.json['size']
    for _ in range(100):
        matrix = [[random.randint(0, 25) for _ in range(size)] for _ in range(size)]
        try:
            HillCipher(matrix)
            return jsonify({'key_matrix': matrix})
        except: continue
    fallback = [[3, 2], [5, 7]] if size == 2 else [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    return jsonify({'key_matrix': fallback})

if __name__ == "__main__":
    app.run(debug=True)