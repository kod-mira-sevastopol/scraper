from flask import Flask, jsonify, request, Blueprint
from controllers.scrab_controller import scrab_controller

app = Flask(__name__)
blueprint = Blueprint('scrab', __name__)

app.register_blueprint(scrab_controller)

@app.route('/')
def hello_world():
    return jsonify('Hello World!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)