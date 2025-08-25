from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    users.append({"email": data["email"], "password": data["password"]})
    return jsonify({"message": "User registered successfully!"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    for u in users:
        if u["email"] == data["email"] and u["password"] == data["password"]:
            return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
