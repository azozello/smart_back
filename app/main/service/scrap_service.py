import mechanize
import http.cookiejar as cookielib
from bs4 import BeautifulSoup
import bs4


def create_scrappers(username, password):
    def scrap_schedule():
        br = set_up_browser()

        if not login(br):
            return 'Invalid credentials.'

        time_table = get_time_table(br)

        days = get_days_rows(time_table)

        formatted_schedule = format_schedule(days)

        return formatted_schedule

    def check_user():
        br = set_up_browser()
        return login(br)

    def set_up_browser():
        # Browser
        brow = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        brow.set_cookiejar(cj)

        # Browser options
        brow.set_handle_equiv(True)
        brow.set_handle_gzip(True)
        brow.set_handle_redirect(True)
        brow.set_handle_referer(True)
        brow.set_handle_robots(False)
        brow.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        brow.addheaders = [('User-agent', 'Chrome')]

        return brow

    def login(brow):
        # The site we will navigate into, handling it's session
        brow.open('https://student.tuke.sk/student/mojePredmetyStudia.mais')

        # Select the second (index one) form (the first form is a search query box)
        brow.select_form(nr=1)

        # User credentials
        brow.form['j_username'] = username
        brow.form['j_password'] = password

        # Login
        response = brow.submit().read()
        soup = BeautifulSoup(response, 'html5lib')
        return soup.find('div', text='Neplatné prihlasovacie údaje') is None

    def get_time_table(br):
        soup = BeautifulSoup(br.open('https://student.tuke.sk/student/rozvrh/show.mais').read(), 'html5lib')
        print(soup.prettify())
        time_table = soup.find('a', attrs={'name': 'JR_PAGE_ANCHOR_0_2'}).contents[1].contents[0].contents[1].contents
        return time_table[5:len(time_table)]

    def get_days_rows(table):
        day_rows = {
            'Pondelok': [],
            'Utorok': [],
            'Streda': [],
            'Štvrtok': [],
            'Piatok': [],
            'Sobota': [],
            'Nedeľa': []
        }
        current_day = 'Pondelok'
        for row in table:
            if row != '\n':
                found_row = row.find('td', attrs={'class': 'orange_bold'})
                if found_row:
                    current_day = found_row.contents[0]
                if current_day == 'Nedeľa':
                    break
                day_rows[current_day].append(row)
        return day_rows

    def format_schedule(days):
        formatted_schedule = []
        current_day = 'Pondelok'

        for day_list in convert_to_days_list(days):
            if type(day_list) is str:
                current_day = day_list
            elif len(day_list) > 0:
                formatted_schedule.append({
                    'day': current_day,
                    'lessons': get_lessons(day_list)
                })

        return formatted_schedule

    def convert_to_days_list(days):
        days_list = []
        for day_rows in days.items():
            for row in day_rows:
                days_list.append(row)
        return days_list

    def get_colspan_translations():
        return {
            1: {'start': '06:45', 'end': '07:30'},
            2: {'start': '07:30', 'end': '08:15'},
            3: {'start': '08:15', 'end': '09:00'},
            4: {'start': '09:10', 'end': '09:55'},
            5: {'start': '09:55', 'end': '10:40'},
            6: {'start': '10:50', 'end': '11:35'},
            7: {'start': '11:35', 'end': '12:20'},
            8: {'start': '12:20', 'end': '13:05'},
            9: {'start': '13:30', 'end': '14:15'},
            10: {'start': '14:15', 'end': '15:00'},
            11: {'start': '15:10', 'end': '15:55'},
            12: {'start': '15:55', 'end': '16:40'},
            13: {'start': '16:50', 'end': '17:35'},
            14: {'start': '17:35', 'end': '18:20'},
            15: {'start': '18:30', 'end': '19:15'},
            16: {'start': '19:15', 'end': '20:00'}
        }

    def parse_description(description_list):
        parsed_description_list = get_parsed_description_list(description_list)
        return description_list_to_json(parsed_description_list)

    def get_parsed_description_list(description_list):
        parsed_description = []
        for description_item in description_list:
            string_content = recursively_get_tags_content(description_item)
            if string_content is not None and string_content != ' ':
                parsed_description.append(string_content)
        return parsed_description

    def description_list_to_json(description_list):
        if len(description_list) == 4:
            return {
                'main': description_list[0],
                'additional': description_list[1],
                'teacher': '',
                'area': description_list[2],
                'type': description_list[3],
                'groups': ''
            }
        elif len(description_list) == 5:
            return {
                'main': description_list[0],
                'additional': '',
                'teacher': description_list[2],
                'area': description_list[1],
                'type': description_list[3],
                'groups': description_list[4]
            }
        else:
            return None

    def recursively_get_tags_content(tag):
        if tag is None or type(tag) == bs4.element.NavigableString:
            return tag
        else:
            if len(tag.contents) > 0:
                return recursively_get_tags_content(tag.contents[0])
            else:
                return None

    def get_lessons(day_rows):
        colspan_translations = get_colspan_translations()
        lessons = []

        skipped_title = False
        for row in day_rows:
            current_time_span = 0
            for content in row.contents:
                if content != '\n' and type(content) == bs4.element.Tag:
                    if not skipped_title:
                        skipped_title = True
                        continue

                    colspan = content.attrs.get('colspan')

                    if content.contents[0] != '\xa0':
                        lessons.append({
                            'start': colspan_translations[current_time_span + 1]['start'],
                            'end': colspan_translations[current_time_span + int(colspan)]['end'],
                            'description': parse_description(content.contents)
                        })

                    if colspan is None:
                        current_time_span += 1
                    else:
                        current_time_span += int(colspan)

        return lessons

    return scrap_schedule, check_user


if __name__ == '__main__':
    # scrap_timetable, _login = create_scrappers('dp330zm', 'a7W8c7U+')
    scrap_timetable, _login = create_scrappers('pc170uy', 'senninha123')
    for day in scrap_timetable():
        print(day)
