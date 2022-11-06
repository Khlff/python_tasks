import re
from collections import defaultdict


class LogParser:
    file = None

    def __init__(self, filename):
        self.file = open(filename, 'r', encoding='cp1251', errors='ignore')

    def get_fastest_page(self):
        max_speed = 0
        while True:
            line = self.file.readline()
            if not line:
                break
            res = re.findall(r'(" (.*?))$', line)
            if res:
                if int(res[0]) > max_speed:
                    max_speed = int(res[0])
        return max_speed

    def get_most_active_client(self, file):
        pass

    def get_most_active_client_by_day(self, file):
        pass

    def get_most_popular_browser(self, file):
        pass

    def get_most_popular_page(self, file):
        pass

    def get_slowest_average_page(self, file):
        pass

    def get_slowest_page(self):
        pass


def main():
    logparser = LogParser("example_1.log")
    print(logparser.get_fastest_page())


if __name__ == '__main__':
    main()
