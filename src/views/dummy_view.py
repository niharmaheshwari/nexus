'''Dummy View'''
import time
from flask import (jsonify, Blueprint)
from src.utils.dummy_view.dummy_data_generate_utils import populate_elastic_search

dummy = Blueprint('test', __name__, url_prefix='/dummy')

@dummy.route('/', methods=['GET'])
def dummy_data_generate():
    '''Dummy Data'''
    populate_elastic_search()
    return jsonify({
        'status':'active',
        'time': time.time()
    })
