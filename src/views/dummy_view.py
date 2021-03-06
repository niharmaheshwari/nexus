'''Dummy View'''
from flask import (jsonify, Blueprint)
from src.utils.dummy_view.dummy_data_generate_utils import populate_elastic_search,\
   populate_dynamo_db

dummy = Blueprint('dummy', __name__, url_prefix='/api/dummy')


@dummy.route('/', methods=['GET'])
def dummy_data_generate():
    '''Dummy Data'''
    populate_elastic_search()
    populate_dynamo_db()
    return jsonify({
        'status': 'success',
    })
