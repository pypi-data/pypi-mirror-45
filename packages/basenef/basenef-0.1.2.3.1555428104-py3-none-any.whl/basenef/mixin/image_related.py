# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: basenef
@file: arithematic_ops.py
@date: 4/13/2019
@desc:
'''
import numpy as np

from .arithematic_ops import ArithematicalOpMixin


class DataClassMixin(ArithematicalOpMixin):
    data: np.ndarray = None


class ShapeMixin(DataClassMixin):
    @property
    def shape(self):
        return np.array(self.data.shape).astype(np.int32)


class LengthMixin(DataClassMixin):
    @property
    def length(self):
        if self.data.shape == 1:
            return len(self.data)
        else:
            return self.data.shape[0]


class CentralSlicesMixin(ShapeMixin):
    @property
    def central_slices(self):
        t0 = self.data[int(self.shape[0] / 2), :, :]
        t1 = self.data[:, int(self.shape[1] / 2), :]
        t2 = self.data[:, :, int(self.shape[2] / 2)]
        return t0, t1, t2


class CentralProfilesMixin(ShapeMixin):
    @property
    def central_profiles(self):
        p0 = self.data[:, int(self.shape[1] / 2), int(self.shape[2] / 2)]
        p1 = self.data[int(self.shape[0] / 2), :, int(self.shape[2] / 2)]
        p2 = self.data[int(self.shape[0] / 2), int(self.shape[1] / 2), :]
        return p0, p1, p2


class ImshowMixin(ShapeMixin):
    def imshow(self, *args, **kwargs):
        from matplotlib import pyplot as plt
        if self.shape == 2:
            plt.imshow(self.data, *args, **kwargs)
        else:
            plt.imshow(self.data[:, :, int(self.shape[2] / 2)], *args, **kwargs)


class Imshow3DMixin(CentralSlicesMixin):
    def imshow3d(self, *args, **kwargs):
        from matplotlib import pyplot as plt
        plt.imshow(self.data, *args, **kwargs)

        plt.subplot(131)
        plt.imshow(self.central_slices[0], *args, **kwargs)
        plt.subplot(132)
        plt.imshow(self.central_slices[1], *args, **kwargs)
        plt.subplot(133)
        plt.imshow(self.central_slices[2], *args, **kwargs)


class UnitSizeMixin(ShapeMixin):
    @property
    def unit_size(self):
        return self.size / self.shape


class Common3DMixin(LengthMixin, CentralProfilesMixin, ImshowMixin, Imshow3DMixin,
                    UnitSizeMixin):
    pass
