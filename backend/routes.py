import re
from flask import Blueprint, request, jsonify, session

from .util import get_prices, update_stores, get_lat_lon
from .services import fetch_locations, parse_stores



prices_bp = Blueprint('prices_bp', __name__)

@prices_bp.route('/prices', methods=['POST'])
def add_to_pricing_queue():
    item_name = request.json.get('item_name')
    zip_code = request.json.get('zip_code')
    
    # update_stores(parse_stores(fetch_locations()))
    
    if not item_name or not zip_code:
        return jsonify({'message': 'Item name and zip code are required'}), 400
    
    if not re.match(r'^\d{5}(-\d{4})?$', zip_code):
        return jsonify({'message': 'Invalid zip code format'}), 400
    
    # check if lat lng for given zip is in session
    lat_lon_key = f'lat_lon_{zip_code}'
    if lat_lon_key not in session:
        lat, lon = get_lat_lon(zip_code)
        session[lat_lon_key] = (lat, lon)
    else:
        lat, lon = session[lat_lon_key]
        
    print(f'lat: {lat}, lon: {lon}')
    
    prices = get_prices(item_name, zip_code, lat, lon)
    
    if not prices:
        return jsonify({'message': f'Prices for {item_name} could not be found'}), 404

    return jsonify(prices), 200

@prices_bp.route('/prices', methods=['GET'])
def retrieve_prices():
    item_names_str = request.args.get('item_names')
    zip_code = request.args.get('zip_code')

    if not item_names_str:
        return jsonify({'message': 'Item names are required'}), 400

    item_names = item_names_str.split(',')
    
    # check if lat lng for given zip is in session
    lat_lon_key = f'lat_lon_{zip_code}'
    if lat_lon_key not in session:
        lat, lon = get_lat_lon(zip_code)
        session[lat_lon_key] = (lat, lon)
    else:
        lat, lon = session[lat_lon_key]
        
    print(f'lat: {lat}, lon: {lon}')
    
    all_prices = {}
    for item in item_names:
        item_prices = get_prices(item, zip_code, lat, lon)
        if item_prices:
            all_prices[item] = item_prices

    return jsonify(all_prices), 200
