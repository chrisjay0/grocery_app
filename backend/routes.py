from flask import Blueprint, request, jsonify
from .util import get_prices

prices_bp = Blueprint('prices_bp', __name__)

@prices_bp.route('/prices', methods=['POST'])
def add_to_pricing_queue():
    print('hello /prices post route activated')
    
    print(request.json)


    item_name = request.json.get('item_name')
    zip_code = request.json.get('zip_code')
    
    if not item_name:
        return jsonify({'message': 'Item name is required'}), 400
    
    prices = get_prices(item_name, zip_code)
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
    
    all_prices = {}
    for item in item_names:
        item_prices = get_prices(item, zip_code)
        if item_prices:
            all_prices[item] = item_prices

    return jsonify(all_prices), 200
