# -*- coding: utf-8 -*-
import sys
import numbers
from . import _bh_api, _info


def _get_dtype_list(operand_list):
    dtype_list = []
    for op in operand_list:
        if isinstance(op, numbers.Number):
            dtype_list.append(None)
        else:
            dtype_list.append(op.base.dtype)

    input_dtype = None
    for dtype in reversed(dtype_list):
        if dtype is not None:
            input_dtype = dtype
            break

    for i in range(len(dtype_list)):
        if dtype_list[i] is None:
            dtype_list[i] = input_dtype
    return dtype_list


class Ufunc(object):
    def __init__(self, info):
        """A Bohrium Universal Function"""
        self.info = info
        if sys.version_info.major >= 3:
            self.__name__ = info['name']
        else:
            # Scipy complains if '__name__' is unicode
            self.__name__ = info['name'].encode('latin_1')

    def __str__(self):
        return "<bohrium Ufunc '%s'>" % self.info['name']

    def __call__(self, operand_list):
        assert (len(operand_list) == self.info["nop"])
        ary_handle_list = []
        for op in operand_list:
            if isinstance(op, numbers.Number):
                ary_handle_list.append(op)
            else:
                assert (op._bhc_handle is not None)
                ary_handle_list.append(op._bhc_handle)
        _bh_api.op(self.info["id"], _get_dtype_list(operand_list), ary_handle_list)


def generate_ufuncs():
    ret = {}
    for op in _info.op.values():
        if op['elementwise']:
            f = Ufunc(op)
            ret[f.info['name']] = f
    return ret


# Generate all ufuncs
ufunc_list = generate_ufuncs()

# Expose them via their names.
for _name, _ufunc in ufunc_list.items():
    exec ("%s = _ufunc" % _name)
