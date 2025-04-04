from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample user data
users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30}
]

# Home Route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to My Flask API!"})

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

# Get a single user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Create a new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "age": data["age"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

# Update an existing user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    user["name"] = data.get("name", user["name"])
    user["age"] = data.get("age", user["age"])
    
    return jsonify(user)

# Delete a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
