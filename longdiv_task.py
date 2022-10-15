#!/usr/bin/env python3


def long_division(dividend, divider):
    '''
    Вернуть строку с процедурой деления «уголком» чисел dividend и divider.
    Формат вывода приведён на примерах ниже.

    Примеры:
    >>> 12345÷25
    12345|25
    100  |493
     234
     225
       95
       75
       20

    >>> 1234÷1423
    1234|1423
    1234|0

    >>> 24600÷123
    24600|123
    246  |200
      0

    >>> 246001÷123
    246001|123
    246   |2000
         1
    '''
    result_of_division = dividend // divider

    if result_of_division == 0:
        return f"{dividend}|{divider}\n{dividend}|0"

    digits = [int(i) for i in str(dividend)]
    answer_string = f"{dividend}|{divider}\n"
    count_of_reminder_output = 0
    rem = offset = 0
    while digits:
        rem = rem * 10 + digits.pop(0)
        if rem >= divider:
            if offset != 0:
                answer_string += f"{' ' * offset}{rem}\n"
            length_of_rem = len(str(rem))
            res = rem // divider
            rem = rem % divider
            if count_of_reminder_output == 0:
                tmp = len(str(dividend)) - len(str(res * divider))
                answer_string += f"{res * divider}" \
                                 f"{' ' * tmp}" \
                                 f"|{result_of_division}\n"
                count_of_reminder_output += 1
            else:
                answer_string += f"{' ' * offset}{res * divider}\n"
                count_of_reminder_output += 1

            offset += length_of_rem - len(str(rem)) + (0 if rem != 0 else 1)
    if rem != 0:
        answer_string += f"{' ' * (len(str(dividend)) - len(str(rem)))}{rem}"
    else:
        answer_string += f"{' ' * (offset - 1)}{rem}"
    return answer_string


def main():
    print(long_division(123, 123))
    print()
    print(long_division(1, 1))
    print()
    print(long_division(15, 3))
    print()
    print(long_division(3, 15))
    print()
    print(long_division(12345, 25))
    print()
    print(long_division(1234, 1423))
    print()
    print(long_division(87654532, 1))
    print()
    print(long_division(24600, 123))
    print()
    print(long_division(4567, 1234567))
    print()
    print(long_division(246001, 123))
    print()
    print(long_division(100000, 50))
    print()
    print(long_division(123456789, 531))
    print()
    print(long_division(425934261694251, 12345678))


if __name__ == '__main__':
    main()
