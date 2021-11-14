<<<<<<< HEAD
"""
Views for authentication APIs
"""
import logging
from flask import request, jsonify, Blueprint
from src.manager.user_manager import UserManager
from src.model.message_format import MessageFormat
from src.utilities.authentication_utils import serialize_user_object

=======
import logging
from flask import Flask, request, jsonify
from src.manager.user_manager import UserManager

app = Flask(__name__)
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)
MANAGER = UserManager()

<<<<<<< HEAD
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/', methods=['GET'])
def init():
    """
    Initialization API call
    """
    return jsonify("Hello World")

@auth.route('/signup', methods=["POST"])
=======
@app.route('/', methods=['GET'])
def init():
    return jsonify("Hello World")

@app.route('/signup', methods=["POST"])
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
def user_signup():
    """
    Allows user to signup and register
    """
    request_body = request.get_json()
    return jsonify(MANAGER.signup(request_body))

<<<<<<< HEAD
@auth.route('/confirm-signup', methods=["POST"])
=======
@app.route('/confirm-signup', methods=["POST"])
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
def user_confirm_signup():
    """
    Confirms user signup with the verification code
    """
    request_body = request.get_json()
    email = request_body["email"]
    code = request_body["code"]
    return jsonify(MANAGER.confirm_signup(email, code))

<<<<<<< HEAD
@auth.route('/login', methods=["POST"])
=======
@app.route('/login', methods=["POST"])
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
def user_login():
    """
    Logs in the user and returns session details
    """
    request_body = request.get_json()
    return jsonify(MANAGER.login(request_body))

<<<<<<< HEAD
@auth.route('/refresh-token', methods=["POST"])
=======
@app.route('/refresh-token', methods=["POST"])
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
def refresh_token():
    """
    Generates new session id and access tokens
    """
    request_body = request.get_json()
    return jsonify(MANAGER.generate_new_token(request_body))

<<<<<<< HEAD
@auth.route('/get-user', methods=["POST"])
=======
@app.route('/get-user', methods=["POST"])
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
def get_user_details():
    """
    Fetches user attributes
    """
    request_body = request.get_json()
    token = request.headers.get("token", None)
    email = request_body.get("email", None)
<<<<<<< HEAD
    response = MANAGER.get_user_details(token, email)
    if response["data"] is not None:
        user_details = serialize_user_object(response["data"]["user"])
        return jsonify(MessageFormat().success_message(\
                    data=user_details))
    return jsonify(response)
=======
    return jsonify(MANAGER.get_user_details(token, email))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
>>>>>>> 9f88c199bb488cc6e1c03c837400ecddc68b9943
