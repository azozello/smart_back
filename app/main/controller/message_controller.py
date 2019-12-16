from flask_restplus import Resource

from ..service.mail_service import get_emails_list
from ..util.dto import MessagesDto

api = MessagesDto.api


@api.route('/')
class Messages(Resource):

    def get(self):
        return get_emails_list()
