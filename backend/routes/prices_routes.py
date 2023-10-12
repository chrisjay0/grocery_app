from flask import Blueprint, request, jsonify, session
from flask_bcrypt import generate_password_hash, check_password_hash
from utilities.prices_utilities import Queue
from database import db
import time
from services.sprouts import fetch_sprouts_prices
from services.food4less import fetch_food4less_prices



prices_bp = Blueprint('prices_bp', __name__)

# Queue to hold products pending price fetch
pricing_queue = Queue()

# In-memory cache to hold fetched prices
prices_cache = {}

@prices_bp.route('/prices', methods=['POST'])
def add_to_pricing_queue():
    item_name = request.json.get('item_name')
    if not item_name:
        print(f'Item name is required. Instead received: {request.json}')
        return jsonify({'message': 'Item name is required'}), 400
    
    # Add item to the queue for price fetching
    pricing_queue.enqueue(item_name)
    
    # Call a function to process the queue (in a real-world scenario, this can be done asynchronously)
    process_queue()
    
    return jsonify({'message': f'Item {item_name} added successfully'}), 200

def process_queue():
    while not pricing_queue.is_empty():
        item_name = pricing_queue.dequeue()
        prices = {
            **fetch_sprouts_prices([item_name]),
            **fetch_food4less_prices([item_name])
        }
        print(f'Fetched prices for {item_name}: {prices}')
        
        # prices appears like
        # {'Sprouts': {'Sprouts 2% Milk': 2.99}, 'Food 4 Less': {'Kroger® Lactose Free 2% Reduced Fat Milk': 3.59}}
        
        # Update the cache with the fetched prices
        prices_cache[item_name] = prices
        
@prices_bp.route('/prices', methods=['GET'])
def get_prices():
    item_names_str = request.args.get('item_names')
    
    if not item_names_str:
        print(f'Item names is required. Instead received: {request.args}')
        return jsonify({'message': 'Item names are required'}), 400
    
    print(item_names_str)

    item_names = item_names_str.split(',')
    
    for item in item_names:
        if item not in prices_cache:
            pricing_queue.enqueue(item)
            process_queue()
            
    prices = {}
    for item in item_names:
        prices[item] = prices_cache[item]
        
    return jsonify(prices), 200
    