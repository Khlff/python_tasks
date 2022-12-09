#!/usr/bin/env python
import math
import sys


def f0():
    a = 3 % 0


def f1():
    print(b)


def f2():
    c = 3 % 0


def f3():
    raise FloatingPointError


def f4():
    math.exp(10, 10000)


def f5():
    h = 435 % 0


def f6():
    assert 2 = 6


def f7():
    list = [1, 2, 4, 5]
    list.b


def f8():
    file.open("lol.txt", "r")


def f9():
    import xccxa


def f10():
    dict = {"lol": "gg", "mmdddd": 2313123}
    dict.abcde


def f11():
    list = [1, 3, 4, 6, 7,0]
    list[12]


def f12():
    dict = {"ggg": "jjj", "mmm": 12345}
    dict[347]


def f13():
    print(j)


def f14():
    date = eval('datetime(2010, 10a, 30)')


def f15():
    a = 5 + "2"



def f16():
    a = chr(1111)
    print(a.encode("ASCII"))



def check_exception(f, exception):
    try:
        f()
    except exception:
        pass
    else:
        print("Bad luck, no exception caught: %s" % exception)
        sys.exit(1)


check_exception(f0, BaseException)
check_exception(f1, Exception)
check_exception(f2, ArithmeticError)
check_exception(f3, FloatingPointError)
check_exception(f4, OverflowError)
check_exception(f5, ZeroDivisionError)
check_exception(f6, AssertionError)
check_exception(f7, AttributeError)
check_exception(f8, EnvironmentError)
check_exception(f9, ImportError)
check_exception(f10, LookupError)
check_exception(f11, IndexError)
check_exception(f12, KeyError)
check_exception(f13, NameError)
check_exception(f14, SyntaxError)
check_exception(f15, ValueError)
check_exception(f16, UnicodeError)

print("Congratulations, you made it!")