from flask import request
from flask_restplus import Resource
from flask import render_template_string

from ..util.dto import MailDto
from ..service.mail_service import get_emails_list, get_email_by_id

api = MailDto.api
_mail = MailDto.mail


@api.route('/')
class Mail(Resource):

    def get(self):
        return get_emails_list()
