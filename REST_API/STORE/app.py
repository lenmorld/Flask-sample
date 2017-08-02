from flask import Flask

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [
            {
                'name': 'Item 1',
                'price': 15.99
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


# POST /store data: {name:}
@app.route('/store', methods=['POST', 'GET'])  # default route is only GET
def create_store():
    pass


# GET /store/<string:name>
# http://127.0.0.1:5000/store/some_name
@app.route('/store/<string:name>')  # name here must match method arg
def get_store(name):
    pass


# GET /store/
# http://127.0.0.1:5000/store/
@app.route('/store')  # name here must match method arg
def get_stores():
    pass


# POST /store/<string:name>/item {name: , price}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    pass


app.run(port=5000)
