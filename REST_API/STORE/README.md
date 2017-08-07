to test:

in General
- browser for GET calls
- use index.html and edit JS httpGetAsync call
- AngularJS
- cURL
- Postman


GET routes

http://127.0.0.1:5000/store
http://127.0.0.1:5000/store/MyStore2
http://127.0.0.1:5000/store/MyStore2/item

- just run in browser
- curl http://127.0.0.1:5000/store


POST routes

Create Store
- curl -X POST  http://127.0.0.1:5000/store --data '{"name": "MyStore3"}' -H "Content-Type: application/json"

Create Item in Store
- curl -X POST  http://127.0.0.1:5000/store/MyStore2/item --data '{"name": "Candy 1", "price": 12.03}' -H "Content-Type: application/json"