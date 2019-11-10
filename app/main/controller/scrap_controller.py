from flask import request
from flask_restplus import Resource

from ..util.dto import TimeTableDto
from ..service.scrap_service import create_scrappers

api = TimeTableDto.api
_time_table = TimeTableDto.time_table


@api.route('/')
class TimeTable(Resource):

    @api.expect(_time_table, Validate=True)
    def post(self):
        data = request.json
        scrap_time_table, login = create_scrappers(data['login'], data['password'])
        return scrap_time_table()
