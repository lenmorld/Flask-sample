from flask import Flask

app = Flask(__name__)


@app.route('/')  # home, method name doesnt matter
def home():
    return "Hello, world!"

app.run(port=5000)
