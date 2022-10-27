import sys, re
from collections import defaultdict


def get_params():
    arg = sys.argv[1]
    return arg


def read_logfile(file_name):
    pass


def get_most_popular_resource():
    count_of_resources = defaultdict(int)
    log_file = open('W3SVC6.log', 'r', encoding='cp1251')
    while True:
        line = log_file.readline()

        if not line:
            break

        resource = re.findall(r'\, (/.*?)\,', line)
        if len(resource) > 0:
            count_of_resources[resource[0]] += 1
    max_frequency = max(count_of_resources.values())
    for k, v in count_of_resources.items():
        if v == max_frequency:
            print(count_of_resources)
            return k
    log_file.close()


def get_most_active_user():
    pass


def main():
    # arg = get_params()
    arg = 'resource'
    if arg == 'resource':
        print(get_most_popular_resource())
    if arg == 'user':
        get_most_active_user()


if __name__ == "__main__":
    main()
