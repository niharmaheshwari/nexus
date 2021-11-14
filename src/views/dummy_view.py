'''Dummy View'''
import time
from flask import (jsonify, Blueprint)
from src.utils.dummy_view.dummy_data_generate_utils import populate_elastic_search, populate_dynamo_db

dummy = Blueprint('test', __name__, url_prefix='/dummy')


@dummy.route('/', methods=['GET'])
def dummy_data_generate():
    '''Dummy Data'''
    populate_elastic_search()
    populate_dynamo_db()
    return jsonify({
        'status': 'success',
        'time': time.time()
    })
