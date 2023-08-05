from ._base import (
    BaseFunction as _BaseFunction,
)


class In(_BaseFunction):
    def __init__(self, collection):
        self.__collection = collection

    def __call__(self, item):
        return item in self.__collection


class Contains(_BaseFunction):
    def __init__(self, item):
        self.__item = item

    def __call__(self, collection):
        return self.__item in collection
