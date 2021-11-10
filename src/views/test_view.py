'''Test View'''
import time
from flask import (jsonify, Blueprint)

test = Blueprint('test', __name__, url_prefix='/test')

@test.route('/', methods=['GET'])
def test_activation():
    '''Base Test'''
    return jsonify({
        'status':'active',
        'time': time.time()
    })

@test.route('/ping', methods=['GET'])
def test_ping():
    '''Test a ping from client'''
    return jsonify({
        'response': 'pong'
    })
