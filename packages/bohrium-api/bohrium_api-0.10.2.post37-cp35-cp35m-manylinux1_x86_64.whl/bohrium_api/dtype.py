# -*- coding: utf-8 -*-
import numpy as np
from . import _bh_api
from ._bh_api import bool, int8, int16, int32, int64, uint8, uint16, uint32, uint64, float32, float64, complex64, \
    complex128

_size_of_dtype_in_bytes = {
    _bh_api.bool: 1,
    _bh_api.int8: 1,
    _bh_api.int16: 2,
    _bh_api.int32: 4,
    _bh_api.int64: 8,
    _bh_api.uint8: 1,
    _bh_api.uint16: 2,
    _bh_api.uint32: 4,
    _bh_api.uint64: 8,
    _bh_api.float32: 4,
    _bh_api.float64: 8,
    _bh_api.complex64: 8,
    _bh_api.complex128: 16,
}

_dtype_bh2np = {
    _bh_api.bool: np.bool,
    _bh_api.int8: np.int8,
    _bh_api.int16: np.int16,
    _bh_api.int32: np.int32,
    _bh_api.int64: np.int64,
    _bh_api.uint8: np.uint8,
    _bh_api.uint16: np.uint16,
    _bh_api.uint32: np.uint32,
    _bh_api.uint64: np.uint64,
    _bh_api.float32: np.float32,
    _bh_api.float64: np.float64,
    _bh_api.complex64: np.complex64,
    _bh_api.complex128: np.complex128,
}

_dtype_np2bh = {
    np.bool: _bh_api.bool,
    np.int8: _bh_api.int8,
    np.int16: _bh_api.int16,
    np.int32: _bh_api.int32,
    np.int64: _bh_api.int64,
    np.uint8: _bh_api.uint8,
    np.uint16: _bh_api.uint16,
    np.uint32: _bh_api.uint32,
    np.uint64: _bh_api.uint64,
    np.float32: _bh_api.float32,
    np.float64: _bh_api.float64,
    np.complex64: _bh_api.complex64,
    np.complex128: _bh_api.complex128,
}

_dtype_str2bh = {
    "bool": _bh_api.bool,
    "int8": _bh_api.int8,
    "int16": _bh_api.int16,
    "int32": _bh_api.int32,
    "int64": _bh_api.int64,
    "uint8": _bh_api.uint8,
    "uint16": _bh_api.uint16,
    "uint32": _bh_api.uint32,
    "uint64": _bh_api.uint64,
    "float32": _bh_api.float32,
    "float64": _bh_api.float64,
    "complex64": _bh_api.complex64,
    "complex128": _bh_api.complex128,
}


def sizeof(dtype):
    """Returns the size of `dtype` (in bytes)"""
    return _size_of_dtype_in_bytes[dtype]


def bh2np(dtype):
    """Convert data type from Bohrium to NumPy"""
    return _dtype_bh2np[dtype]


def np2bh(dtype):
    """Convert data type from NumPy to Bohrium"""
    return _dtype_np2bh[dtype]


def str2bh(dtype_as_string):
    """Convert data type from String to Bohrium"""
    return _dtype_np2bh[dtype_as_string.lower()]
