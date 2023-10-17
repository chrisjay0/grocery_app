# test_routes.py

import json

def test_add_to_pricing_queue(client, db):
    # Mock data to send in the request
    data = {
        "item_name": "apple",
        "zip_code": "90001"
    }

    # Make a POST request to the /prices route
    response = client.post("/prices", data=json.dumps(data), content_type="application/json")
    print(type(response))
    print(response)

    # Ensure the response has a 200 status code (success)
    assert response.status_code == 200

def test_empty_item_name(client, db):
    data = {
        "item_name": "",
        "zip_code": "90001"
    }
    response = client.post("/prices", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "Item name and zip code are required" in response.get_data(as_text=True)

def test_invalid_zip_code_format(client, db):
    data = {
        "item_name": "apple",
        "zip_code": "9000a"
    }
    response = client.post("/prices", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    # Assuming your service returns a specific error message for invalid zip codes
    # Adjust the assertion below based on your actual error message
    assert "Invalid zip code format" in response.get_data(as_text=True)

def test_missing_item_name(client, db):
    data = {
        "zip_code": "90001"
    }
    response = client.post("/prices", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "Item name and zip code are required" in response.get_data(as_text=True)

def test_missing_zip_code(client, db):
    data = {
        "item_name": "apple"
    }
    response = client.post("/prices", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    # Assuming your service returns a specific error message for missing zip codes
    # Adjust the assertion below based on your actual error message
    assert "Item name and zip code are required" in response.get_data(as_text=True)

def test_non_existing_item(client, db):
    data = {
        "item_name": "notARealItem",
        "zip_code": "90001"
    }
    response = client.post("/prices", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    assert f'Prices for {data["item_name"]} could not be found' in response.get_data(as_text=True)
    
def test_retrieve_prices_single_item(client, db):
    response = client.get("/prices?item_names=apple&zip_code=90001")
    assert response.status_code == 200
    data = response.get_json()
    assert "apple" in data
    
def test_retrieve_prices_missing_item_names(client, db):
    response = client.get("/prices?zip_code=90001")
    assert response.status_code == 400
    assert "Item names are required" in response.get_data(as_text=True)

def test_retrieve_prices_multiple_items(client, db):
    response = client.get("/prices?item_names=apple,orange&zip_code=90001")
    assert response.status_code == 200
    data = response.get_json()
    assert "apple" in data
    assert "orange" in data

def test_retrieve_prices_item_not_found(client, db):
    response = client.get("/prices?item_names=nonexistentitem&zip_code=90001")
    assert response.status_code == 200
    data = response.get_json()
    assert "nonexistentitem" not in data
