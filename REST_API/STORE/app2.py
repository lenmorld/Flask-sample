from flask import Flask, jsonify, request, render_template


app = Flask(__name__)

stores = [
    {
        'name': 'MyStore',
        'items': [
            {
                'name': 'Item 1',
                'price': 15.99
            }
        ]
    },
    {
        'name': 'MyStore2',
        'items': [
            {
                'name': 'Item A',
                'price': 22.50
            }
        ]
    },
    {
        'name': 'My Store With Spaces',
        'items': [
            {
                'name': 'Item A1',
                'price': 50.99
            }
        ]
    }
]

# POST - server is receiving data
# GET - server sends back data

# endpoints

# POST /store data: {name:}
# GET /store/<string:name>
# GET /store
# POST /store/<string:name>/item {name: , price}
# GET /store/<string:name>/item


#HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')            # index.html should be in templates folder


# POST /store data: {name:}
@app.route('/store', methods=['POST'])  # default route is only GET, can also be ['POST', 'GET']
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)



# GET /store/<string:name>
# http://127.0.0.1:5000/store/some_name
@app.route('/store/<string:name>')  # name here must match method arg
def get_store(name):
    # iterate over stores, and find matching one and return it
    # if no match return error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({"message": "Store not found"})


# GET /store/
# http://127.0.0.1:5000/store/
@app.route('/store')  # name here must match method arg
def get_stores():
    return jsonify({'stores': stores})      # stores list [] to json {} to JSON string (using jsonify)

# POST /store/<string:name>/item {name: , price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()


    # iterate over stores, and find matching one
    # if no match return error message
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({"message": "Store not found"})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    # iterate over stores, and find matching one and return its items
    # if no match return error message
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({"message": "Store not found"})


app.run(port=5000)
