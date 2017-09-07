from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Resource is the Class to be instantiated as object

class Student(Resource):
    def get(self, name):
        return {'student': name}

# this is equivalent to app.route() decorator
api.add_resource(Student, '/student/<string:name>')     # http://localhost:5000/student/Len

app.run(port=5000)

    # def post(self):
