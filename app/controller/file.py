
from flask import Blueprint, send_from_directory
from app.service.user import PROFILE_IMAGE_PATH

app = Blueprint('file', __name__)

@app.route('/user/<int:userId>/profile/image', methods=['GET'])
def controlGetUserProfileImage(userId):
	try:
		return send_from_directory(PROFILE_IMAGE_PATH, '{}.png'.format(userId))
	except Exception as e:
		print e
		return 'no image'