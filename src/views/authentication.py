import logging
from flask import Flask, request, jsonify
from src.manager.user_manager import UserManager

app = Flask(__name__)
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)
MANAGER = UserManager()

@app.route('/', methods=['GET'])
def init():
    return jsonify("Hello World")

@app.route('/signup', methods=["POST"])
def user_signup():
    """
    Allows user to signup and register
    """
    request_body = request.get_json()
    return jsonify(MANAGER.signup(request_body))

@app.route('/confirm-signup', methods=["POST"])
def user_confirm_signup():
    """
    Confirms user signup with the verification code
    """
    request_body = request.get_json()
    email = request_body["email"]
    code = request_body["code"]
    return jsonify(MANAGER.confirm_signup(email, code))

@app.route('/login', methods=["POST"])
def user_login():
    """
    Logs in the user and returns session details
    """
    request_body = request.get_json()
    return jsonify(MANAGER.login(request_body))

@app.route('/refresh-token', methods=["POST"])
def refresh_token():
    """
    Generates new session id and access tokens
    """
    request_body = request.get_json()
    return jsonify(MANAGER.generate_new_token(request_body))

@app.route('/get-user', methods=["POST"])
def get_user_details():
    """
    Fetches user attributes
    """
    request_body = request.get_json()
    token = request.headers.get("token", None)
    email = request_body.get("email", None)
    return jsonify(MANAGER.get_user_details(token, email))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
