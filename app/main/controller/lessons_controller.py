from flask_restplus import Resource

from ..util.dto import LessonsDto

import json

api = LessonsDto.api


@api.route('/')
class Messages(Resource):

    def get(self):
        return json.loads(
            '[{"type":"1.ročník","courses":[{"id":"1","title":"Inteligentné systémy v informatike","isLocked":false,"content":[{"week":"23 september - 29 september","links":[{"type":"pdf","label":"Lecture 1.2","url":"https://www.apple.com/"},{"type":"word","label":"Working form for planning of the first simulation","url":"https://www.apple.com/"},{"type":"excel","label":"AMEISE project planning templateSúbor","url":"https://www.apple.com/"}]},{"week":"30 september - 6 október","links":[{"type":"pdf","label":"Lecture 1.2","url":"https://www.apple.com/"}]},{"week":"7 október - 13 október","links":[{"type":"task","label":"FP+COCOMO results","url":"https://www.apple.com/"}]},{"week":"14 október - 20 október","links":[{"type":"link","label":"The link to the Flash videos from the lecture slidesURL","url":"https://www.apple.com/"}]}]},{"id":"2","title":"Bakalárska práca","isLocked":true},{"id":"3","title":"Vývoj počítačových hier","isLocked":true},{"id":"4","title":"Používateľské rozhrania programových systémov","isLocked":true},{"id":"5","title":"Asembler","isLocked":true}]},{"type":"2.ročník","courses":[{"id":"6","title":"Inteligentné systémy v informatike","isLocked":true},{"id":"7","title":"Bakalárska práca","isLocked":true},{"id":"8","title":"Vývoj počítačových hier","isLocked":true}]},{"type":"3.ročník","courses":[{"id":"9","title":"Inteligentné systémy v informatike","isLocked":true},{"id":"10","title":"Bakalárska práca","isLocked":true},{"id":"11","title":"Vývoj počítačových hier","isLocked":true}]},{"type":"4.ročník","courses":[{"id":"12","title":"Inteligentné systémy v informatike","isLocked":true},{"id":"13","title":"Bakalárska práca","isLocked":true}]},{"type":"5.ročník","courses":[{"id":"14","title":"Inteligentné systémy v informatike","isLocked":false,"content":[{"week":"23 september - 29 september","links":[{"type":"pdf","label":"Lecture 1.2","url":"https://www.apple.com/"},{"type":"word","label":"Working form for planning of the first simulation","url":"https://www.apple.com/"},{"type":"excel","label":"AMEISE project planning templateSúbor","url":"https://www.apple.com/"}]},{"week":"30 september - 6 október","links":[{"type":"pdf","label":"Lecture 1.2","url":"https://www.apple.com/"}]},{"week":"7 október - 13 október","links":[{"type":"task","label":"FP+COCOMO results","url":"https://www.apple.com/"}]},{"week":"14 október - 20 október","links":[{"type":"link","label":"The link to the Flash videos from the lecture slidesURL","url":"https://www.apple.com/"}]}]}]}]')
