# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: basenef
@file: arithematic_ops.py
@date: 4/13/2019
@desc:
'''
import operator
import numpy as np
from copy import copy


class UnaryOpMixin:
    def abs(self):
        return self._replace(data = np.abs(self.data))

    def __neg__(self):
        return self._replace(data = -self.data)


class BinaryOpMixin:
    def __eq__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data + other)
        else:
            return self._replace(data = self.data + other.data)

    def __gt__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data > other)
        else:
            return self._replace(data = self.data > other.data)

    def __ge__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data >= other)
        else:
            return self._replace(data = self.data >= other.data)

    def __lt__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data < other)
        else:
            return self._replace(data = self.data < other.data)

    def __le__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data <= other)
        else:
            return self._replace(data = self.data <= other.data)

    def __add__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data + other)
        else:
            return self._replace(data = self.data + other.data)

    def __sub__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data - other)
        else:
            return self._replace(data = self.data - other.data)

    def __mul__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data * other)
        else:
            return self._replace(data = self.data * other.data)

    def __truediv__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            new_data = self.data / other
        else:
            new_data = self.data / other.data
        new_data[new_data == np.inf] = 0.0
        return self._replace(data = new_data)

    def __floordiv__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data // other)
        else:
            return self._replace(data = self.data // other.data)

    def __mod__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data % other)
        else:
            return self._replace(data = self.data % other.data)

    def __pow__(self, other):
        if np.isscalar(other) or isinstance(other, np.ndarray):
            return self._replace(data = self.data ** other)
        else:
            return self._replace(data = self.data ** other.data)


class ArithematicalOpMixin(BinaryOpMixin, UnaryOpMixin):
    pass
