from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class TimeTableDto:
    api = Namespace('TimeTable', description='data used to login in mais system')
    time_table = api.model('time_table', {
        'login': fields.String(required=True),
        'password': fields.String(required=True)
    })


class MessagesDto:
    api = Namespace('Messages', description='data used in email system')
    mail = api.model('messages', {})


class LessonsDto:
    api = Namespace('Lessons', description='data used in lessons system')
