# -*- coding: utf-8 -*-
import operator
import functools
import numpy as np
from . import _bh_api, _info
from . import dtype as _dtype


class BhBase(object):
    def __init__(self, dtype, nelem):
        self._bhc_handle = None
        self.dtype = dtype
        self.nelem = nelem
        self.itemsize = _dtype.sizeof(dtype)
        self.nbytes = nelem * self.itemsize
        self._bhc_handle = _bh_api.new(dtype, self.nelem)

    def __del__(self):
        if self._bhc_handle is not None:
            _bh_api.destroy(self.dtype, self._bhc_handle)

    def __str__(self):
        return str(self.toNumPy())

    def toNumPy(self):
        _bh_api.flush()
        data = _bh_api.data_get(self.dtype, self._bhc_handle, True, True, False, self.nbytes)
        return np.frombuffer(data, dtype=_dtype.bh2np(self.dtype))


class BhArray(object):
    def __init__(self, shape, dtype, stride=None, offset=0, base=None):
        self._bhc_handle = None
        self.nelem = functools.reduce(operator.mul, shape)
        if base is None:
            base = BhBase(dtype, self.nelem)
        assert(dtype == base.dtype)
        if stride is None:
            stride = [0] * len(shape)
            s = 1
            for i in range(len(shape)):
                stride[len(shape) - i - 1] = s
                s *= shape[i]
        self.base = base
        self.shape = tuple(shape)
        self.stride = tuple(stride)
        self.offset = offset
        self._bhc_handle = _bh_api.view(dtype, base._bhc_handle, len(shape), int(offset), list(shape), list(stride))

    def __del__(self):
        if self._bhc_handle is not None:
            _bh_api.destroy(self.base.dtype, self._bhc_handle)

    def __str__(self):
        return str(self.toNumPy())

    def toNumPy(self):
        data = self.base.toNumPy()
        if self.offset > 0:
            data = data[self.offset:]
        return np.lib.stride_tricks.as_strided(data, shape=self.shape,
                                               strides=[s * self.base.itemsize for s in self.stride])
