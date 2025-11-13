#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> raisins = LineItem('Golden raisins', 10, 6.95)
>>> raisins.weight, raisins.description, raisins.price
(10, 'Golden raisins', 6.95)
>>> raisins.subtotal()
69.5
>>> raisins.weight = -20
Traceback (most recent call last):
    ...
ValueError: -20 must be > 0
>>> raisins.weight
10
>>> raisins = LineItem('Golden raisins', 10, 6.95)
>>> dir(raisins)[:3]
['NonBlank#description', 'Quantity#price', 'Quantity#weight']
>>> LineItem.description.storage_name
'NonBlank#description'
>>> raisins.description
'Golden raisins'
>>> getattr(raisins, 'NonBlank#description')
'Golden raisins'
>>> LineItem.weight  # doctest: +ELLIPSIS
<__main__.Quantity object at 0x...>
>>> LineItem.weight.storage_name
'Quantity#weight'
>>> br_nuts = LineItem('Brazil Nuts', 10, 34.95)
>>> br_nuts.description = ' '
Traceback (most recent call last):
    ...
ValueError: str must be not empty or blank
>>> void = LineItem('', 1, 1)
Traceback (most recent call last):
    ...
ValueError: str must be not empty or blank
>>> for name in LineItem.iter_fields():
...     print(name)
...
description
weight
price

"""
from typing import Iterator, Any
from abc import ABC, abstractmethod


class Descriptor:
    # def __set_name__(self, owner, name):
    #     self.storage_name = f"{self.__class__.__name__}#{name}"
    def __init__(self, name=None):
        self.storage_name = name

    def __get__(self, instance, owner):
        if not instance:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        value = self.validate(value)
        setattr(instance, self.storage_name, value)


class Validated(ABC, Descriptor):
    @abstractmethod
    def validate(self, value):
        pass


class Quantity(Validated):
    def validate(self, value):
        if value < 0:
            raise ValueError(f"{value} must be > 0")
        return value


class NonBlank(Validated):
    def validate(self, value):
        value = value.strip()
        if not value:
            raise ValueError("str must be not empty or blank")
        return value


class EntityMeta(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        fields = []
        for name, value in clsdict.items():
            if isinstance(value, Descriptor):
                descriptor = value
                descriptor.storage_name = f"{descriptor.__class__.__name__}#{name}"
                fields.append(name)
        setattr(cls, "_field_names", fields)


class Entity(metaclass=EntityMeta):
    @classmethod
    def iter_fields(cls) -> Iterator[str]:
        for name in cls._field_names:
            yield name


class LineItem(Entity):
    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


def as_tuple(line_item: LineItem) -> tuple[Any, ...]:
    return tuple(line_item.__dict__.values())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
