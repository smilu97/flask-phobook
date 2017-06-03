from flask import Blueprint, jsonify

app = Blueprint('base', __name__)


@app.route('/', methods=['GET'])
def controlHome():
    return 'ok'


@app.route('/test', methods=['GET'])
def controlTest():
    return jsonify({'success': 1, 'msg': 'modified'})
