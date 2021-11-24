'''Client View'''
from flask import (jsonify, Blueprint, render_template, send_from_directory)
from src.utils.dummy_view.dummy_data_generate_utils import populate_elastic_search,\
   populate_dynamo_db

client = Blueprint('client', __name__, url_prefix='/')

@client.route('/manifest.json')
def manifest():
    '''Assets page'''
    return send_from_directory('./build', 'asset-manifest.json')


@client.route('/favicon.ico')
def favicon():
    '''Favicon page'''
    return send_from_directory('./build', 'favicon.ico')

@client.route('/')
def home():
    '''home page'''
    return render_template('index.html')
    
