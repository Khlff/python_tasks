import re
import sys
from collections import defaultdict


def get_params():
    file_name = sys.argv[1]
    function_name = sys.argv[2]
    return file_name, function_name


def open_file(file_name):
    file = open(file_name, 'r', encoding='cp1251', errors='ignore')
    return file


def make_stat(regular_expression, file_name):
    stat_dict = defaultdict(int)
    file = open_file(file_name)
    while True:
        line = file.readline()
        if not line:
            break

        founded_element = re.findall(regular_expression, line)
        if len(founded_element) > 0:
            stat_dict[founded_element[0]] += 1

    max_frequency = max(stat_dict.values())
    for key, value in stat_dict.items():
        if value == max_frequency:
            file.close()
            return key


def get_most_popular_resource(file_name):
    return make_stat(r'\, (/.*?)\,', file_name)


def get_most_active_user(file_name):
    return make_stat(r'^(\d*?\.\d*?\.\d*?\.\d*?),', file_name)


def main():
    args = get_params()
    input_log_filename = args[0]
    func_name = args[1]
    if func_name == 'resource':
        print(get_most_popular_resource(input_log_filename))
    if func_name == 'user':
        print(get_most_active_user(input_log_filename))


if __name__ == "__main__":
    main()
