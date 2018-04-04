# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify, request


api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
def search():
    lat = float(request.args.get('lat', None).strip())
    lng = float(request.args.get('lng', None).strip())
    radius = int(request.args.get('radius', None).strip())
    count = int(request.args.get('count', None).strip())
    tags = request.args.getlist('tags[]', None)
    
    return jsonify({'products': []})
