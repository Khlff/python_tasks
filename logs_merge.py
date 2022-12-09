import re
import unittest
from collections import defaultdict
from datetime import datetime


def merge(*iterables, key=lambda x: x):
    """Функция склеивает упорядоченные по ключу `key` и порядку «меньше»
    коллекции из `iterables`.

    Результат — итератор на упорядоченные данные.
    В случае равенства данных следует их упорядочить в порядке следования
    коллекций"""

    ordered_map = defaultdict()
    for iterable in iterables:
        sorted_iter = iter(sorted(iterable, key=lambda x: key(x)))
        try:
            ordered_map[sorted_iter] = next(sorted_iter)
        except StopIteration:
            pass

    while ordered_map:
        res = min(ordered_map.items(), key=lambda x: key(x[1]))
        yield res[1]

        try:
            ordered_map[res[0]] = next(res[0])
        except StopIteration:
            del ordered_map[res[0]]


def log_key(log_string):
    """Функция по строке лога возвращает ключ для её сравнения по времени"""

    raw_datetime = re.findall(r'.*?\[(.*?) [\+-].*?\]', log_string)
    if raw_datetime:
        return datetime.strptime(raw_datetime[0], '%d/%b/%Y:%H:%M:%S')
    return datetime(9999, 1, 1, 1, 1, 1, 1)


class TestTest(unittest.TestCase):
    def test_log_key_first(self):
        log_string = '192.168.12.61 - - [29/Jan/2012:06:40:26 +0600] "GET /'
        self.assertEqual(datetime(2012, 1, 29, 6, 40, 26),
                         log_key(log_string))

    def test_log_key_second(self):
        log_string = '192.168.12.61 - - [29/Jan/2013:06:40:26 +0600] "GET /'
        self.assertEqual(datetime(2013, 1, 29, 6, 40, 26),
                         log_key(log_string))

    def test_log_key_wrong_input(self):
        log_string = 'amogus'
        self.assertEqual(datetime(9999, 1, 1, 1, 1, 1, 1), log_key(log_string))

    def test_merge(self):
        iter1 = ['192.168.12.204 - - [18/Feb/2013:06:40:28 +0600] "GET '
                 '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 986',
                 '192.168.74.151 - - [17/Feb/2013:06:40:30 +0600] "GET '
                 '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 987']

        iter2 = ['192.168.12.210 - - [19/Feb/2013:06:40:35 +0600] "GET '
                 '/pause/ajaxPause?pauseCongId=all&admin=1 HTTP/1.1" 200 1047']

        result = ['192.168.74.151 - - [17/Feb/2013:06:40:30 +0600] "GET '
                  '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 987',
                  '192.168.12.204 - - [18/Feb/2013:06:40:28 +0600] "GET '
                  '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 986',
                  '192.168.12.210 - - [19/Feb/2013:06:40:35 +0600] "GET '
                  '/pause/ajaxPause?pauseCongId=all&admin=1 HTTP/1.1" 200 1047'
                  ]

        counter = 0
        for elem in merge(iter1, iter2, key=log_key):
            self.assertEqual(result[counter], elem)
            counter += 1

    def test_merge_with_equals(self):
        iter1 = ['192.168.12.204 - - [18/Feb/2013:06:40:28 +0600] "GET '
                 '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 986',
                 '192.168.74.151 - - [17/Feb/2013:06:40:30 +0600] "GET '
                 '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 987']

        iter2 = ['192.168.12.204 - - [18/Feb/2013:06:40:28 +0600] "GET '
                 '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 986']

        result = ['192.168.74.151 - - [17/Feb/2013:06:40:30 +0600] "GET '
                  '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 987',
                  '192.168.12.204 - - [18/Feb/2013:06:40:28 +0600] "GET '
                  '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 986',
                  '192.168.12.204 - - [18/Feb/2013:06:40:28 +0600] "GET '
                  '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 986',
                  ]

        counter = 0
        for elem in merge(iter1, iter2, key=log_key):
            self.assertEqual(result[counter], elem)
            counter += 1

    def test_merge_with_empty_strings(self):
        iter1 = ['',
                 '192.168.12.204 - - [18/Feb/2013:06:40:28 +0600] "GET '
                 '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 986']

        result = ['192.168.12.204 - - [18/Feb/2013:06:40:28 +0600] "GET '
                  '/pause/ajaxPause?pauseConfigId=&admin=0 HTTP/1.1" 200 986',
                  '']

        counter = 0
        for elem in merge(iter1, key=log_key):
            self.assertEqual(result[counter], elem)
            counter += 1


if __name__ == '__main__':
    unittest.main()