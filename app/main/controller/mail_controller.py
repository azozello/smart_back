from flask_restplus import Resource

from ..service.mail_service import get_emails_list
from ..util.dto import MailDto

api = MailDto.api


@api.route('/')
class Mail(Resource):

    def get(self):
        return get_emails_list()
