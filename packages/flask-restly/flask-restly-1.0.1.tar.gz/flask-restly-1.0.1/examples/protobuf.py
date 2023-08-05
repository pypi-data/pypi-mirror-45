from flask import Flask
from flask_restly import FlaskRestly
from flask_restly.decorator import resource, get, body, post
from flask_restly.serializer import protobuf
# generated message
from dsl_pb2 import DslEntity

app = Flask(__name__)

app.config['RESTLY_SERIALIZER'] = protobuf

rest = FlaskRestly(app)
rest.init_app(app)


@resource(name='employees')
class EmployeesResource:
    @get('/<int:id>')
    @body(DslEntity)
    # @body(outgoing=Employee)
    def get_employee(self, id):
        he = dict(a="av", b="bv")
        return dict(body=b"example", headers={'Name': 'Zara', 1: 'Nope'})


with app.app_context():
    EmployeesResource()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
