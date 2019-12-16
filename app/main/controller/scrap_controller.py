from flask import request
from flask_restplus import Resource

from ..service.scrap_service import create_scrappers
from ..util.dto import TimeTableDto

api = TimeTableDto.api
_time_table = TimeTableDto.time_table


@api.route('/')
class TimeTable(Resource):

    @api.expect(_time_table, Validate=True)
    def post(self):
        data = request.json
        try:
            scrap_time_table, login = create_scrappers(data['login'], data['password'])
            return scrap_time_table()
        except Exception as e:
            return [{
                "day": "Error",
                "lessons": [
                    {
                        "start": "07:30",
                        "end": "09:00",
                        "description": {
                            "main": str(e),
                            "additional": "",
                            "teacher": "",
                            "area": "",
                            "type": "",
                            "groups": ""
                        }
                    },
                ]
            }]
