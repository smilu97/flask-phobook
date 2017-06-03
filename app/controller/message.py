# -*- coding: utf8 -*-

from flask import Blueprint, request, jsonify
from flask_login import current_user
from app.service import assert_login

import app.service.message as service

app = Blueprint('message', __name__)


@app.route('/contact/<int:contactId>/message', methods=['POST'])
def controlPostMessage(contactId):
    try:
        assert_login()
        json = request.get_json()
        content = json['content']
        message = service.create(current_user, contactId, content)
        return jsonify({'success': 1, 'message': message.serialize})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})


@app.route('/contact/<int:contactId>/messages', methods=['GET'])
def controlGetMessages(contactId):
    try:
        assert_login()
        messages = service.find_all(current_user, contactId)
        return jsonify({'success': 1, 'messages': [i.serialize for i in messages]})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})
