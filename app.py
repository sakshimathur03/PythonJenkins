from flask import Flask, request, jsonify
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, title="Flask API with Swagger", version="1.0", description="A simple Flask API with Swagger UI")

# Create a namespace
ns = api.namespace("users", description="User operations")

# Sample user data
users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30}
]

# User model for Swagger documentation
from flask_restx import fields
user_model = api.model("User", {
    "id": fields.Integer(readOnly=True, description="User ID"),
    "name": fields.String(required=True, description="User Name"),
    "age": fields.Integer(required=True, description="User Age")
})

# Home Route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to My Flask API!"})

# User API Routes
@ns.route("/")
class UserList(Resource):
    @ns.doc("Get all users")
    @ns.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        return users

    @ns.doc("Create a new user")
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = api.payload
        new_user = {
            "id": len(users) + 1,
            "name": data["name"],
            "age": data["age"]
        }
        users.append(new_user)
        return new_user, 201

@ns.route("/<int:user_id>")
@ns.param("user_id", "The user ID")
@ns.response(404, "User not found")
class User(Resource):
    @ns.doc("Get a user by ID")
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """Get a specific user by ID"""
        user = next((u for u in users if u["id"] == user_id), None)
        if user:
            return user
        api.abort(404, "User not found")

    @ns.doc("Update a user")
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """Update an existing user"""
        user = next((u for u in users if u["id"] == user_id), None)
        if user:
            data = api.payload
            user["name"] = data.get("name", user["name"])
            user["age"] = data.get("age", user["age"])
            return user
        api.abort(404, "User not found")

    @ns.doc("Delete a user")
    @ns.response(200, "User deleted successfully")
    def delete(self, user_id):
        """Delete a user"""
        global users
        users = [u for u in users if u["id"] != user_id]
        return {"message": "User deleted successfully"}, 200

if __name__ == "__main__":
    app.run(debug=True)
