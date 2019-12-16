from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.scrap_controller import api as scrap_ns
from .main.controller.mail_controller import api as mail_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(scrap_ns, path='/scrap')
api.add_namespace(mail_ns, path='/mail_list')
api.add_namespace(auth_ns)
