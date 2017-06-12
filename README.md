# PHOBOOK

Author:

* 김영진 (smilup2244@gmail.com)
* 이진명 (jinious1111@naver.com)

## Description

한양대학교 객체지향설계 수업 4번째 Term Project 제출용 프로젝트 입니다. 전화번호부를 기초 컨셉으로 합니다.

(https://book.smilu.link) 와 연동하는 API 서버 입니다.

## What we used

* Flask
  * Flask-cors
  * Flask-login
* Flask-socketio
* PyMysql (MySQL으로 테스트 되어있습니다. 이것은 MySQL과 Python을 연결해주는 드라이버 이며, 다른 DB를 쓸 경우 대체되야 합니다)
* SQLAlchemy
* gevent

## How to setup

Virtualenv 가 설치를 권장합니다. virtualenv설치에 대해서는 이 사이트를 참고하세요 [Go](https://virtualenv.pypa.io/en/stable/)

```sh
git clone https://github.com/smilu97/oop_term_flask
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
uwsgi wsgi.ini
```

Virtualenv가 설치되있지 않은 경우 위에서 2, 3번째 줄을 생략하여 아래와 같이 실행합니다

```sh
git clone https://github.com/smilu97/oop_term_flask
pip install -r requirements.txt
uwsgi wsgi.ini
```

### UWSGI Setting

[wsgi.ini](./wsgi.ini) 를 참고하세요. uwsgi는 플라스크 어플리케이션과 nginx, tomcat과 같은 서버가 통신할 수 있도록 연결해줍니다.

## Configurations

[config.py](./config.py)를 참고하세요. Database와 관련된 설정은 DATABASE_CONNECT_URL 만 잘 설정되있으면 문제없이 돌아갑니다.

DATABASE_CONNECT_URL에는 유저정보, 패스워드, 호스트, 포트, 데이터베이스, 스키마, 등등 접속에 필요한 모든 정보가 한꺼번에 들어가야합니다.
