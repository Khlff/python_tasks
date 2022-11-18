import re
import unittest
from collections import defaultdict
import datetime

month_number = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9,
                'Oct': 10, 'Nov': 11, 'Dec': 12}


class LogLineHandler:
    def __init__(self, raw_string):
        self._compiled_regular_expression = re.compile(
            r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r' - - \['
            r'(\d{1,2})/'
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/'
            r'(\d{4}):(\d{1,2}):(\d{1,2}):(\d{1,2})'
            r'.*?\] .*? '
            r'(/.*?) '
            r'.* \d{3}.*?" "'
            r'(.*?)"'
            r' ?(\n|\d+)?'
        )
        _result = self._compiled_regular_expression.findall(raw_string)
        if len(_result) != 0:
            _result = _result[0]
            self.client = _result[0]
            self.date = datetime.date(int(_result[3]),
                                      month_number[_result[2]],
                                      int(_result[1]))
            self.page = _result[7]
            self.browser = _result[8]
            self.connection_time = _result[9]
            self.error = 0
        else:
            self.error = 1


class LogStatistic:
    def __init__(self):
        self._statistic = {"browser": defaultdict(int),
                           "client_activity_by_all_time": defaultdict(int),
                           "page": defaultdict(int),
                           "client_activity_by_days": defaultdict(dict),
                           "page_speed": defaultdict(list),
                           }

    def _get_max_value_of_dictionary(self, dictionary_name):
        return max(self._statistic[dictionary_name].values())

    def processing(self, log_line_handled: LogLineHandler):
        if log_line_handled.error != 1:
            self._statistic['browser'][log_line_handled.browser] += 1

            self._statistic['client_activity_by_all_time'][
                log_line_handled.client] += 1

            self._statistic['page'][log_line_handled.page] += 1

            if log_line_handled.client in (
                    self._statistic['client_activity_by_days'][
                        log_line_handled.date].keys()):
                self._statistic['client_activity_by_days'][
                    log_line_handled.date][
                    log_line_handled.client] += 1
            else:
                self._statistic['client_activity_by_days'][
                    log_line_handled.date][
                    log_line_handled.client] = 1

            if log_line_handled.connection_time:
                self._statistic['page_speed'][
                    log_line_handled.page].append(
                    int(log_line_handled.connection_time))

                if "fastest_page" in self._statistic.keys():
                    if self._statistic["fastest_page"][1] >= int(
                            log_line_handled.connection_time):
                        self._statistic["fastest_page"] = (
                            log_line_handled.page,
                            int(log_line_handled.connection_time))

                else:
                    self._statistic["fastest_page"] = (
                        log_line_handled.page,
                        int(log_line_handled.connection_time))

                if "slowest_page" in self._statistic.keys():
                    if self._statistic["slowest_page"][1] <= int(
                            log_line_handled.connection_time):
                        self._statistic["slowest_page"] = (
                            log_line_handled.page,
                            int(log_line_handled.connection_time))

                else:
                    self._statistic["slowest_page"] = (
                        log_line_handled.page,
                        int(log_line_handled.connection_time))

    def get_most_active_client_by_all_time(self):
        if self._statistic["client_activity_by_all_time"] == {}:
            return ""

        max_value = (
            self._get_max_value_of_dictionary("client_activity_by_all_time"))

        if list(self._statistic["client_activity_by_all_time"].values()).count(
                max_value) > 1:
            client = ""

            for key, value in (self._statistic["client_activity_by_all_time"]
                                   .items()):
                if value == max_value and client == "":
                    client = key
                elif client > key:
                    client = key

            return client

        else:
            for key, value in (self._statistic["client_activity_by_all_time"]
                                   .items()):
                if value == max_value:
                    return key

    def get_most_popular_browser(self):
        if self._statistic["browser"] == {}:
            return ""

        max_count = self._get_max_value_of_dictionary("browser")

        if list(self._statistic["browser"].values()).count(max_count) > 1:
            browser = ""

            for key, value in self._statistic["browser"].items():
                if value == max_count and browser == "":
                    browser = key

                else:
                    if browser > key:
                        browser = key

            return browser
        else:
            for key, value in self._statistic["browser"].items():
                if value == max_count:
                    return key

    def get_most_popular_page(self):
        if self._statistic["page"] == {}:
            return ""

        max_count = self._get_max_value_of_dictionary("page")

        if list(self._statistic["page"].values()).count(max_count) > 1:
            page = ""
            for key, value in self._statistic["page"].items():
                if value == max_count and page == "":
                    page = key

                elif value == max_count:
                    if page > key:
                        page = key

            return page
        else:
            for key, value in self._statistic["page"].items():
                if value == max_count:
                    return key

    def get_fastest_page(self):
        if 'fastest_page' not in self._statistic.keys():
            return ""

        return self._statistic['fastest_page'][0]

    def get_slowest_page(self):
        if 'slowest_page' not in self._statistic.keys():
            return ""

        return self._statistic['slowest_page'][0]

    def get_slowest_average_page(self):
        if self._statistic['page_speed'] == {}:
            return ''

        slowest_page = ("", 0)
        for page in self._statistic['page_speed'].keys():
            average_page_speed = (sum(self._statistic['page_speed'][page])
                                  / len(self._statistic['page_speed'][page]))
            if average_page_speed > slowest_page[1]:
                slowest_page = (page, average_page_speed)
        return slowest_page[0]

    def get_most_active_client_by_days(self):
        if self._statistic['client_activity_by_days'] == {}:
            return {}

        result = {}
        for date in self._statistic['client_activity_by_days'].keys():
            max_per_date = max(
                self._statistic['client_activity_by_days'][date].values())

            if list(self._statistic['client_activity_by_days'][date]
                        .values()).count(max_per_date) > 1:
                client = ""

                for key, value in (
                        self._statistic['client_activity_by_days'][date]
                            .items()):
                    if value == max_per_date and client == "":
                        client = value
                    elif client > key:
                        client = key

                result[date] = client

            else:
                for key, value in (
                        self._statistic['client_activity_by_days'][date]
                            .items()):
                    if value == max_per_date:
                        result[date] = key
        return result


class Analyzer:
    def __init__(self):
        self.log_statistic = LogStatistic()

    def add_line(self, line):
        self.log_statistic.processing(LogLineHandler(line))

    def results(self) -> dict:
        statistic = self.log_statistic

        result = {
            'FastestPage':
                statistic.get_fastest_page(),
            'MostActiveClient':
                statistic.get_most_active_client_by_all_time(),
            'MostActiveClientByDay':
                statistic.get_most_active_client_by_days(),
            'MostPopularBrowser':
                statistic.get_most_popular_browser(),
            'MostPopularPage':
                statistic.get_most_popular_page(),
            'SlowestAveragePage':
                statistic.get_slowest_average_page(),
            'SlowestPage':
                statistic.get_slowest_page()
        }
        return result


def make_stat():
    return Analyzer()


class LogStatTests(unittest.TestCase):
    def test_empty_log(self) -> None:
        statistic = make_stat()

        expected = {
            'FastestPage': '',
            'MostActiveClient': '',
            'MostActiveClientByDay': {},
            'MostPopularBrowser': '',
            'MostPopularPage': '',
            'SlowestAveragePage': '',
            'SlowestPage': ''
        }

        self.assertDictEqual(expected, statistic.results())

    def test_incorrect_lines(self) -> None:
        statistic = make_stat()

        statistic.add_line('Not a log line. Don`t know how to handle it')
        statistic.add_line('')
        statistic.add_line('1121212332')

        expected = {
            'FastestPage': '',
            'MostActiveClient': '',
            'MostActiveClientByDay': {},
            'MostPopularBrowser': '',
            'MostPopularPage': '',
            'SlowestAveragePage': '',
            'SlowestPage': ''
        }

        self.assertDictEqual(expected, statistic.results())

    def test_correct_logs_plus_incorrect(self) -> None:
        statistic = make_stat()

        statistic.add_line('Not a log line. Don`t know how to handle it')
        statistic.add_line('')
        statistic.add_line('1121212332')

        statistic.add_line('127.0.0.1 - - [08/Jul/2012:06:27:38 +0600] '
                           '"OPTIONS * HTTP/1.0" 200 152 '
                           '"-" '
                           '"Apache/2.2.16 (Debian)'
                           ' (internal dummy connection)" '
                           '58')

        statistic.add_line('192.168.74.5 - - [08/Jul/2012:06:27:51 +0600] '
                           '"GET /menu-top.php HTTP/1.1" '
                           '200 2522 "-" '
                           '"Mozilla/4.0 (compatible; MSIE 7.0; '
                           'Windows NT 6.1; WOW64; Trident/5.0; '
                           'SLCC2; .NET CLR 2.0.50727; '
                           '.NET CLR 3.5.30729; '
                           '.NET CLR 3.0.30729; '
                           'Media Center PC 6.0; '
                           'InfoPath.3; '
                           '.NET4.0C; '
                           'MS-RTC LM 8)" '
                           '21288')
        expected = {'FastestPage': '/menu-top.php',
                    'MostActiveClient': '192.168.74.5',
                    'MostActiveClientByDay':
                        {datetime.date(2012, 7, 8): '192.168.74.5'},
                    'MostPopularBrowser': 'Mozilla/4.0 (compatible; '
                                          'MSIE 7.0; '
                                          'Windows NT 6.1; '
                                          'WOW64; Trident/5.0; '
                                          'SLCC2; '
                                          '.NET CLR 2.0.50727; '
                                          '.NET CLR 3.5.30729; '
                                          '.NET CLR 3.0.30729; '
                                          'Media Center PC 6.0; '
                                          'InfoPath.3; '
                                          '.NET4.0C; MS-RTC LM 8)',
                    'MostPopularPage': '/menu-top.php',
                    'SlowestAveragePage': '/menu-top.php',
                    'SlowestPage': '/menu-top.php'}

        self.assertDictEqual(expected, statistic.results())

    def test_lines_without_connection_time(self) -> None:
        statistic = make_stat()

        statistic.add_line('127.0.0.1 - - [08/Jul/2012:06:27:38 +0600] '
                           '"OPTIONS * HTTP/1.0" 200 152 '
                           '"-" '
                           '"Apache/2.2.16 (Debian)'
                           ' (internal dummy connection)"')

        statistic.add_line('192.168.74.5 - - [08/Jul/2012:06:27:51 +0600] '
                           '"GET /menu-top.php HTTP/1.1" '
                           '200 2522 "-" '
                           '"Mozilla/4.0 (compatible; MSIE 7.0; '
                           'Windows NT 6.1; WOW64; Trident/5.0; '
                           'SLCC2; .NET CLR 2.0.50727; '
                           '.NET CLR 3.5.30729; '
                           '.NET CLR 3.0.30729; '
                           'Media Center PC 6.0; '
                           'InfoPath.3; '
                           '.NET4.0C; '
                           'MS-RTC LM 8)" '
                           '21288')

        expected = {'FastestPage': '/menu-top.php',
                    'MostActiveClient': '192.168.74.5',
                    'MostActiveClientByDay':
                        {datetime.date(2012, 7, 8): '192.168.74.5'},
                    'MostPopularBrowser': 'Mozilla/4.0 (compatible; '
                                          'MSIE 7.0; '
                                          'Windows NT 6.1; '
                                          'WOW64; '
                                          'Trident/5.0; '
                                          'SLCC2; '
                                          '.NET CLR 2.0.50727; '
                                          '.NET CLR 3.5.30729; '
                                          '.NET CLR 3.0.30729; '
                                          'Media Center PC 6.0; '
                                          'InfoPath.3; '
                                          '.NET4.0C; '
                                          'MS-RTC LM 8)',
                    'MostPopularPage': '/menu-top.php',
                    'SlowestAveragePage': '/menu-top.php',
                    'SlowestPage': '/menu-top.php'}

        self.assertDictEqual(expected, statistic.results())
