# -*- coding: utf8 -*-

from flask import Blueprint, request, jsonify
from flask_login import current_user
from app.service import assert_login

import app.service.user as service

app = Blueprint('user', __name__)


@app.route('/login', methods=['POST'])
def controlPostLogin():
    try:
        json = request.get_json()
        phoneNumber = json['phoneNumber']
        password = json['password']
        user = service.login(phoneNumber, password)
        res = user.serialize
        res['token'] = user.token
        return jsonify({'success': 1, 'user': res})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})

@app.route('/whoami', methods=['GET'])
def controlWhoami():
    try:
        if current_user.is_anonymous:
            raise Exception(u'로그인에 실패했습니다. 전화번호나 비밀번호가 맞는지 다시 확인해주세요')
        res = current_user.serialize
        res['token'] = current_user.token
        return jsonify({'success': 1, 'user': res})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})


@app.route('/signup', methods=['POST'])
def controlSignup():
    try:
        json = request.get_json()
        user = service.signup(json)
        return jsonify({'success': 1, 'user': user.serialize})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})


@app.route('/checkuser/<string:phoneNumber>', methods=['GET'])
def controlGetCheckUser(phoneNumber):
    try:
        user = service.findByPhoneNumber(phoneNumber)
        if user and user.password:
            return jsonify({'success': 1, 'exist': True})
        else:
            return jsonify({'success': 1, 'exist': False})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': u'조회에 실패했습니다'})


@app.route('/contact', methods=['POST'])
def controllPostContact():
    try:
        assert_login()
        json = request.get_json()
        phoneNumber = json['phoneNumber']
        name = json['name']
        other = service.createContact(current_user, name, phoneNumber)
        return jsonify({'success': 1, 'otherId': other.id})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})


@app.route('/contact/<int:contactId>', methods=['GET'])
def controlGetContact(contactId):
    try:
        assert_login()
        contact = service.get(contactId)
        if not contact:
            raise u'잘못된 사용자 번호입니다'
        if contact not in current_user.contacts:
            raise u'접근이 불가합니다'
        return jsonify({'success': 1, 'contact': contact.serialize})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})


# @app.route('/contacts/<int:page>', methods=['GET'])
# def controlGetContacts(page):
#   try:
#       assertLogin()
#       contacts = service.getContacts(current_user, page, **(request.args))
#       return jsonify({'success': 1, 'contacts': [i.serialize for i in contacts]})
#   except Exception as e:
#       print e
#       return jsonify({'success': 0, 'error': str(e)})


@app.route('/contacts/all', methods=['GET'])
def controlGetContactsAll():
    try:
        args = request.args
        limit = int(args.get('limit', 999999))
        assert_login()
        return jsonify({'success': 1, 'contacts': [i.serialize for i in current_user.contacts[:limit]]})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})


@app.route('/contact/<int:otherId>', methods=['DELETE'])
def controlDeletePutContact(otherId):
    try:
        assert_login()
        if not service.removeContact(current_user, otherId):
            raise Exception(u'삭제에 실패했습니다')
        return jsonify({'success': 1})
    except Exception as e:
        print e
        return jsonify({'success': 0, 'error': str(e)})
