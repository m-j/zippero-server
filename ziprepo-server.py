from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

hello = {'hello': 'World'}

class HelloWorld(Resource):
    def get(self):
        return hello

    def post(self):
        global hello
        payload = request.get_json()
        hello = payload
        print(payload)

        return 'ok'


api.add_resource(HelloWorld, '/hello')

if __name__ == '__main__':
    app.run(port=7001, debug=True)