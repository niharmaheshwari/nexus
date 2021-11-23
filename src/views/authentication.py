"""
Views for authentication APIs
"""
import logging
from flask import request, jsonify, Blueprint
from src.manager.user_manager import UserManager
from src.model.message_format import MessageFormat
from src.utilities.authentication_utils import serialize_user_object
from src.utilities.authorization import authorization

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)
MANAGER = UserManager()

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/', methods=['GET'])
def init():
    """
    Initialization API call
    """
    return jsonify("Hello World")

@auth.route('/signup', methods=["POST"])
def user_signup():
    """
    Allows user to signup and register
    """
    request_body = request.get_json()
    return jsonify(MANAGER.signup(request_body))

@auth.route('/confirm-signup', methods=["POST"])
def user_confirm_signup():
    """
    Confirms user signup with the verification code
    """
    request_body = request.get_json()
    email = request_body["email"]
    code = request_body["code"]
    return jsonify(MANAGER.confirm_signup(email, code))

@auth.route('/login', methods=["POST"])
def user_login():
    """
    Logs in the user and returns session details
    """
    request_body = request.get_json()
    return jsonify(MANAGER.login(request_body))

@auth.route('/refresh-token', methods=["POST"])
def refresh_token():
    """
    Generates new session id and access tokens
    """
    request_body = request.get_json()
    return jsonify(MANAGER.generate_new_token(request_body))

@auth.route('/get-user', methods=["GET"])
@authorization
def get_user_details():
    """
    Fetches user attributes
    """
    id_token = request.headers.get("token", None)
    response = MANAGER.get_user_details(id_token)
    if response["data"] is not None:
        user_details = serialize_user_object(response["data"]["user"])
        return jsonify(MessageFormat().success_message(\
                    data=user_details))
    return jsonify(response)
