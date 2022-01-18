from qlat.lat_io import *
from qlat.rng_state import *

import math
import copy
import numpy as np

alpha_qed = 1.0 / 137.035999084
fminv_gev = 0.197326979

class use_kwargs:

    def __init__(self, kwargs):
        self.default_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def f(*args, **kwargs):
            if "is_default_kwargs_applied" not in kwargs:
                kwargs = self.default_kwargs | kwargs
            return func(*args, **kwargs)
        return f

# ----------

def interpolate_list(v, i):
    size = len(v)
    i1 = math.floor(i)
    assert i1 >= 0
    i2 = i1 + 1
    if i2 >= size:
        return v[size - 1]
    elif i1 < 0:
        return v[0]
    v1 = v[i1]
    v2 = v[i2]
    a1 = i2 - i
    a2 = i - i1
    return a1 * v1 + a2 * v2

def interpolate(v_arr, i_arr):
    vt = v_arr.transpose()
    return np.array([ interpolate_list(vt, i) for i in i_arr ]).transpose()

def partial_sum_list(x, *, is_half_last = False):
    """Modify in-place"""
    s = 0
    for i, v in enumerate(x):
        sp = s
        s += v
        if is_half_last:
            x[i] = (s + sp) / 2
        else:
            x[i] = s

def partial_sum(x, *, is_half_last = False):
    shape = x.shape
    if len(shape) == 0:
        return
    elif len(shape) == 1:
        partial_sum_list(x, is_half_last = is_half_last)
    elif len(shape) == 2:
        for v in x:
            partial_sum_list(v, is_half_last = is_half_last)
    else:
        assert False

def check_zero(x):
    if isinstance(x, (int, float, complex)) and 0 == x:
        return True
    return False

class Data:

    def __init__(self, val):
        # supported value types:
        # numeric
        # numpy.array
        # q.LatData
        if isinstance(val, Data):
            self.val = val.val
            assert not isinstance(self.val)
        else:
            self.val = val

    def __str__(self):
        return f"Data({self.val})"

    def get_val(self):
        return self.val

    def __copy__(self):
        return Data(copy.copy(self.val))

    def __deepcopy__(self, memo):
        return Data(copy.deepcopy(self.val, memo))

    def __add__(self, other):
        if isinstance(other, Data):
            if check_zero(self.val):
                return other
            elif check_zero(other.val):
                return self
            else:
                return Data(self.val + other.val)
        else:
            return self + Data(other)

    __radd__ = __add__

    def __mul__(self, other):
        if isinstance(other, Data):
            if check_zero(self.val) or check_zero(other.val):
                return Data(0)
            return Data(self.val * other.val)
        else:
            return self * Data(other)

    def __rmul__(self, other):
        if isinstance(other, Data):
            assert False
            return None
        else:
            return Data(other) * self

    def __neg__(self):
        return Data(-self.val)

    def __pos__(self):
        return self

    def __sub__(self, other):
        if isinstance(other, Data):
            if check_zero(self.val):
                return Data(-other.val)
            elif check_zero(other.val):
                return self
            else:
                return Data(self.val - other.val)
        else:
            return self - Data(other)

    def __rsub__(self, other):
        if isinstance(other, Data):
            assert False
            return None
        else:
            return Data(other) - self

# ----------

def add_jk_idx(arr):
    # arr: no jk index
    # return: add trivial jk index in the LAST axis
    return arr.reshape(arr.shape + (1,))

def jk_transpose(arr):
    # arr: jk index is the 0th axis
    # return: jk index is the last axis
    shape = arr.shape
    ndim = len(shape)
    if ndim <= 1:
        return arr
    axes = list(range(1, ndim)) + [ 0, ]
    return arr.transpose(axes)

def jk_transpose_back(arr):
    # jk_transpose_back(jk_transpose(arr)) == arr
    shape = arr.shape
    ndim = len(shape)
    if ndim <= 1:
        return arr
    axes = [ ndim - 1, ] + list(range(0, ndim - 1))
    return arr.transpose(axes)

def average(data_list):
    n = len(data_list)
    v = sum(data_list)
    return 1/n * v

def jackknife(data_list, eps = 1):
    # normal jackknife uses eps = 1
    data_list_real = [ d for d in data_list if d is not None ]
    n = len(data_list_real)
    fac = eps / n
    avg = average(data_list_real)
    jks = [ avg, ]
    for data in data_list:
        if data is None:
            jks.append(avg)
        else:
            jks.append(avg + fac * (data - avg))
    return jks

def fsqr(data):
    if isinstance(data, (float, int,)):
        return data * data
    elif isinstance(data, complex):
        r = data.real
        i = data.imag
        return complex(r * r, i * i)
    elif isinstance(data, np.ndarray):
        if data.dtype in [ np.float, np.int, ]:
            return np.square(data)
        elif data.dtype in [ np.complex, ]:
            return np.square(data.real) + 1j * np.square(data.imag)
        else:
            raise Exception(f"fsqr data={data} type not supported")
    elif isinstance(data, Data):
        return Data(fsqr(data.val))
    else:
        raise Exception(f"fsqr data={data} type not supported")

def fsqrt(data):
    if isinstance(data, (float, int,)):
        return math.sqrt(data)
    elif isinstance(data, complex):
        r = data.real
        i = data.imag
        return complex(math.sqrt(r), math.sqrt(i))
    elif isinstance(data, np.ndarray):
        if data.dtype in [ np.float, np.int, ]:
            return np.sqrt(data)
        elif data.dtype in [ np.complex, ]:
            return np.sqrt(data.real) + 1j * np.sqrt(data.imag)
        else:
            raise Exception(f"fsqr data={data} type not supported")
    elif isinstance(data, Data):
        return Data(fsqrt(data.val))
    else:
        raise Exception(f"fsqr {data} type not supported")

def jk_avg(jk_list):
    return jk_list[0]

def jk_err(jk_list, eps = 1):
    # same eps as the eps used in the 'jackknife' function
    avg = jk_avg(jk_list)
    diff_sqr = average([ fsqr(jk - avg) for jk in jk_list[1:] ])
    return (math.sqrt(len(jk_list) - 1) / eps) * fsqrt(diff_sqr)

def jk_avg_err(jk_list, eps = 1):
    return jk_avg(jk_list), jk_err(jk_list, eps)

def merge_jk_idx(*jk_idx_list):
    for jk_idx in jk_idx_list:
        assert jk_idx[0] == "avg"
    return [ "avg", ] + [ idx for jk_idx in jk_idx_list for idx in jk_idx[1:] ]

def rejk_list(jk_list, jk_idx, all_jk_idx):
    # super jackknife
    assert jk_idx[0] == "avg"
    assert all_jk_idx[0] == "avg"
    assert len(jk_idx) == len(jk_list)
    assert len(jk_idx) <= len(all_jk_idx)
    jk_avg = jk_list[0]
    size_new = len(all_jk_idx)
    i_new = 0
    jk_list_new = []
    for i, idx in enumerate(jk_idx):
        while all_jk_idx[i_new] != idx:
            jk_list_new.append(jk_avg)
            i_new += 1
            assert i_new < size_new
        jk_list_new.append(jk_list[i])
        i_new += 1
    while i_new < size_new:
        jk_list_new.append(jk_avg)
        i_new += 1
    assert i_new == size_new
    assert size_new == len(jk_list_new)
    return jk_list_new

# ----------

def rjk_jk_list(jk_list, jk_idx, n_rand_sample, rng_state = None):
    # return rjk_list
    # len(rjk_list) == 1 + n_rand_sample
    # distribution of rjk_list should be similar as the distribution of avg
    # r_{i,j} ~ N(0, 1)
    # avg = jk_avg(jk_list)
    # n = len(jk_list)
    # rjk_list[i] = avg + \sum_{j=1}^{n-1} r_{i,j} (jk_list[j] - avg)
    assert jk_idx[0] == "avg"
    assert isinstance(n_rand_sample, int)
    assert n_rand_sample >= 0
    if rng_state is None:
        rng_state = RngState("rjk_list")
    else:
        assert isinstance(rng_state, RngState)
    rs = rng_state
    avg = jk_avg(jk_list)
    n = len(jk_list) - 1
    jk_diff = [ jk_list[j] - avg for j in range(1, n) ]
    rjk_list = [ avg, ]
    for i in range(n_rand_sample):
        rsi = rs.split(i)
        r = [ rsi.split(idx).g_rand_gen() for idx in jk_idx[1:] ]
        rjk_list.append(avg + sum([ r[j] * jk_diff[j] for j in range(n - 1) ]))
    return rjk_list

def rjackknife(data_list, jk_idx, n_rand_sample, rng_state = None, *, eps = 1):
    jk_list = jackknife(data_list, eps)
    return rjk_jk_list(jk_list, jk_idx, n_rand_sample, rng_state)

def rjk_avg(rjk_list):
    return jk_avg(rjk_list)

def rjk_err(rjk_list, eps = 1):
    return jk_err(rjk_list, eps * np.sqrt(len(rjk_list)))

def rjk_avg_err(rjk_list, eps = 1):
    return rjk_avg(rjk_list), rjk_err(rjk_list, eps)

# ----------

default_g_jk_kwargs = {}
default_g_jk_kwargs["jk_type"] = "rjk"  # choices: "rjk", "super"
default_g_jk_kwargs["n_rand_sample"] = 1024
default_g_jk_kwargs["rng_state"] = None
default_g_jk_kwargs["eps"] = 1

@use_kwargs(default_g_jk_kwargs)
def g_jk(data_list, *, eps, **kwargs):
    return jackknife(data_list, eps)

@use_kwargs(default_g_jk_kwargs)
def g_rejk(jk_list, jk_idx, *, jk_type, **kwargs):
    # jk_type in [ "rjk", "super", ]
    if jk_type == "super":
        all_jk_idx = kwargs["all_jk_idx"]
        return rejk_list(jk_list, jk_idx, all_jk_idx)
    elif jk_type == "rjk":
        n_rand_sample = kwargs["n_rand_sample"]
        rng_state = kwargs["rng_state"]
        return rjk_jk_list(jk_list, jk_idx, n_rand_sample, rng_state)
    else:
        assert False
    return None

def g_jk_avg(jk_list):
    return jk_avg(jk_list)

@use_kwargs(default_g_jk_kwargs)
def g_jk_err(jk_list, *, eps, jk_type, **kwargs):
    if jk_type == "super":
        return jk_err(jk_list, eps)
    elif jk_type == "rjk":
        return rjk_err(jk_list, eps)
    else:
        assert False
    return None

def g_jk_avg_err(jk_list, **kwargs):
    return g_jk_avg(jk_list), g_jk_err(jk_list, **kwargs)
