from flask import Blueprint 

app = Blueprint('base', __name__)

@app.route('/', methods=['GET'])
def controlHome():
	return 'ok'