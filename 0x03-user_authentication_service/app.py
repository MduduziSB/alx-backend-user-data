#!/usr/bin/env python3
""" Basic Flask app module """
from flask import Flask, jsonify, redirect, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index() -> str:
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user() -> str:
    """ Function that implements the POST /users route. """
    email = request.form["email"]
    password = request.form["password"]

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """ Function to respond to the POST /sessions route. """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ logout function to respond to the DELETE /sessions route """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
