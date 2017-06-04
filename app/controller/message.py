# -*- coding: utf8 -*-

from flask import Blueprint, request, jsonify
from flask_login import current_user
from app.service import assert_login

import app.service.message as service
import app.service.user as userService

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
        other = userService.get(contactId)
        if not other:
            raise Exception(u'존재하지 않는 유저입니다')
        return jsonify({'success': 1, 'messages': [i.serialize for i in messages], \
            'user': other.serialize})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})
