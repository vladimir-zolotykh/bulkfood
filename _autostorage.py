#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> a = A()
>>> a.storage_name
'_A#0'
>>> b = B()
>>> b.storage_name
'_B#1'
"""


class AutoStorage:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = "_{}#{}".format(prefix, index)
        cls.__counter += 1


class A(AutoStorage):
    pass


class B(A):
    pass


if __name__ == "__main__":
    import doctest

    doctest.testmod()
