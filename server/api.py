# -*- coding: utf-8 -*-
from searchProvider import SearchProvider
from location import Location
from flask import Blueprint, current_app, jsonify, request
from decimal import Decimal
from customExceptions import InputError
import sys

api = Blueprint('api', __name__)

#add these two variables to config
maximumRadius = 2000
maximumProductCount = 50

def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
def search():
    try:
        lat = float(request.args.get('lat', None).strip())
        lng = float(request.args.get('lng', None).strip())
        radius = int(request.args.get('radius', None).strip())
        count = int(request.args.get('count', None).strip())
        tags = request.args.getlist('tags[]', None)
    except ValueError as e:
        exc_info = sys.exc_info()
        raise InputError, InputError(e), exc_info[2]

    #maybe return more information than just inputerror. Such as "maximum allowed radius is 2000" etc...
    if abs(lat)>90 or abs(lng)>180 or radius <= 0 or count <=0 or radius>maximumRadius or count>maximumProductCount:
        raise InputError
    
    provider = SearchProvider(current_app.Locator)

    results = provider.Search(lat,lng,radius,set(tags),count)

    res = []
    for result in results:
        res.append({"Title":result.Product.title,"Popularity":result.Product.popularity,"Lat":result.Shop.lat,"Lng":result.Shop.lng})
        
    return jsonify(res)
