'''Dummy View'''
import time
from flask import (jsonify, Blueprint)

dummy = Blueprint('test', __name__, url_prefix='/dummy')

@dummy.route('/', methods=['GET'])
def dummy_data_generate():
    '''Dummy Data'''
    
    return jsonify({
        'status':'active',
        'time': time.time()
    })
