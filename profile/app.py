from flask import Flask, request, jsonify

app = Flask(__name__)

profiles = []

@app.route('/profile', methods=['POST'])
def add_profile():
    data = request.get_json()
    profiles.append(data)
    return jsonify({"message": "Profile added successfully!"})

@app.route('/profile', methods=['GET'])
def get_profiles():
    return jsonify(profiles)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
