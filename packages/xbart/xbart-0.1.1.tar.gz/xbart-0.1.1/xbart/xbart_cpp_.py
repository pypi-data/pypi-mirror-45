# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_xbart_cpp_')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_xbart_cpp_')
    _xbart_cpp_ = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_xbart_cpp_', [dirname(__file__)])
        except ImportError:
            import _xbart_cpp_
            return _xbart_cpp_
        try:
            _mod = imp.load_module('_xbart_cpp_', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _xbart_cpp_ = swig_import_helper()
    del swig_import_helper
else:
    import _xbart_cpp_
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0


import collections

class XBARTcppParams(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, XBARTcppParams, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, XBARTcppParams, name)
    __repr__ = _swig_repr
    __swig_setmethods__["M"] = _xbart_cpp_.XBARTcppParams_M_set
    __swig_getmethods__["M"] = _xbart_cpp_.XBARTcppParams_M_get
    if _newclass:
        M = _swig_property(_xbart_cpp_.XBARTcppParams_M_get, _xbart_cpp_.XBARTcppParams_M_set)
    __swig_setmethods__["N_sweeps"] = _xbart_cpp_.XBARTcppParams_N_sweeps_set
    __swig_getmethods__["N_sweeps"] = _xbart_cpp_.XBARTcppParams_N_sweeps_get
    if _newclass:
        N_sweeps = _swig_property(_xbart_cpp_.XBARTcppParams_N_sweeps_get, _xbart_cpp_.XBARTcppParams_N_sweeps_set)
    __swig_setmethods__["Nmin"] = _xbart_cpp_.XBARTcppParams_Nmin_set
    __swig_getmethods__["Nmin"] = _xbart_cpp_.XBARTcppParams_Nmin_get
    if _newclass:
        Nmin = _swig_property(_xbart_cpp_.XBARTcppParams_Nmin_get, _xbart_cpp_.XBARTcppParams_Nmin_set)
    __swig_setmethods__["Ncutpoints"] = _xbart_cpp_.XBARTcppParams_Ncutpoints_set
    __swig_getmethods__["Ncutpoints"] = _xbart_cpp_.XBARTcppParams_Ncutpoints_get
    if _newclass:
        Ncutpoints = _swig_property(_xbart_cpp_.XBARTcppParams_Ncutpoints_get, _xbart_cpp_.XBARTcppParams_Ncutpoints_set)
    __swig_setmethods__["burnin"] = _xbart_cpp_.XBARTcppParams_burnin_set
    __swig_getmethods__["burnin"] = _xbart_cpp_.XBARTcppParams_burnin_get
    if _newclass:
        burnin = _swig_property(_xbart_cpp_.XBARTcppParams_burnin_get, _xbart_cpp_.XBARTcppParams_burnin_set)
    __swig_setmethods__["mtry"] = _xbart_cpp_.XBARTcppParams_mtry_set
    __swig_getmethods__["mtry"] = _xbart_cpp_.XBARTcppParams_mtry_get
    if _newclass:
        mtry = _swig_property(_xbart_cpp_.XBARTcppParams_mtry_get, _xbart_cpp_.XBARTcppParams_mtry_set)
    __swig_setmethods__["max_depth_num"] = _xbart_cpp_.XBARTcppParams_max_depth_num_set
    __swig_getmethods__["max_depth_num"] = _xbart_cpp_.XBARTcppParams_max_depth_num_get
    if _newclass:
        max_depth_num = _swig_property(_xbart_cpp_.XBARTcppParams_max_depth_num_get, _xbart_cpp_.XBARTcppParams_max_depth_num_set)
    __swig_setmethods__["alpha"] = _xbart_cpp_.XBARTcppParams_alpha_set
    __swig_getmethods__["alpha"] = _xbart_cpp_.XBARTcppParams_alpha_get
    if _newclass:
        alpha = _swig_property(_xbart_cpp_.XBARTcppParams_alpha_get, _xbart_cpp_.XBARTcppParams_alpha_set)
    __swig_setmethods__["beta"] = _xbart_cpp_.XBARTcppParams_beta_set
    __swig_getmethods__["beta"] = _xbart_cpp_.XBARTcppParams_beta_get
    if _newclass:
        beta = _swig_property(_xbart_cpp_.XBARTcppParams_beta_get, _xbart_cpp_.XBARTcppParams_beta_set)
    __swig_setmethods__["tau"] = _xbart_cpp_.XBARTcppParams_tau_set
    __swig_getmethods__["tau"] = _xbart_cpp_.XBARTcppParams_tau_get
    if _newclass:
        tau = _swig_property(_xbart_cpp_.XBARTcppParams_tau_get, _xbart_cpp_.XBARTcppParams_tau_set)
    __swig_setmethods__["kap"] = _xbart_cpp_.XBARTcppParams_kap_set
    __swig_getmethods__["kap"] = _xbart_cpp_.XBARTcppParams_kap_get
    if _newclass:
        kap = _swig_property(_xbart_cpp_.XBARTcppParams_kap_get, _xbart_cpp_.XBARTcppParams_kap_set)
    __swig_setmethods__["s"] = _xbart_cpp_.XBARTcppParams_s_set
    __swig_getmethods__["s"] = _xbart_cpp_.XBARTcppParams_s_get
    if _newclass:
        s = _swig_property(_xbart_cpp_.XBARTcppParams_s_get, _xbart_cpp_.XBARTcppParams_s_set)
    __swig_setmethods__["verbose"] = _xbart_cpp_.XBARTcppParams_verbose_set
    __swig_getmethods__["verbose"] = _xbart_cpp_.XBARTcppParams_verbose_get
    if _newclass:
        verbose = _swig_property(_xbart_cpp_.XBARTcppParams_verbose_get, _xbart_cpp_.XBARTcppParams_verbose_set)
    __swig_setmethods__["draw_mu"] = _xbart_cpp_.XBARTcppParams_draw_mu_set
    __swig_getmethods__["draw_mu"] = _xbart_cpp_.XBARTcppParams_draw_mu_get
    if _newclass:
        draw_mu = _swig_property(_xbart_cpp_.XBARTcppParams_draw_mu_get, _xbart_cpp_.XBARTcppParams_draw_mu_set)
    __swig_setmethods__["parallel"] = _xbart_cpp_.XBARTcppParams_parallel_set
    __swig_getmethods__["parallel"] = _xbart_cpp_.XBARTcppParams_parallel_get
    if _newclass:
        parallel = _swig_property(_xbart_cpp_.XBARTcppParams_parallel_get, _xbart_cpp_.XBARTcppParams_parallel_set)
    __swig_setmethods__["seed"] = _xbart_cpp_.XBARTcppParams_seed_set
    __swig_getmethods__["seed"] = _xbart_cpp_.XBARTcppParams_seed_get
    if _newclass:
        seed = _swig_property(_xbart_cpp_.XBARTcppParams_seed_get, _xbart_cpp_.XBARTcppParams_seed_set)

    def __init__(self):
        this = _xbart_cpp_.new_XBARTcppParams()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _xbart_cpp_.delete_XBARTcppParams
    __del__ = lambda self: None
XBARTcppParams_swigregister = _xbart_cpp_.XBARTcppParams_swigregister
XBARTcppParams_swigregister(XBARTcppParams)

class XBARTcpp(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, XBARTcpp, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, XBARTcpp, name)
    __repr__ = _swig_repr

    def __init__(self, *args):
        this = _xbart_cpp_.new_XBARTcpp(*args)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this

    def sort_x(self, n: 'int', size: 'int') -> "void":
        return _xbart_cpp_.XBARTcpp_sort_x(self, n, size)

    def _fit_predict(self, n: 'int', n_y: 'int', n_test: 'int', size: 'int', p_cat: 'size_t') -> "void":
        return _xbart_cpp_.XBARTcpp__fit_predict(self, n, n_y, n_test, size, p_cat)

    def _predict(self, n: 'int') -> "void":
        return _xbart_cpp_.XBARTcpp__predict(self, n)

    def _fit(self, n: 'int', n_y: 'int', p_cat: 'size_t') -> "void":
        return _xbart_cpp_.XBARTcpp__fit(self, n, n_y, p_cat)

    def get_M(self) -> "int":
        return _xbart_cpp_.XBARTcpp_get_M(self)

    def get_N_sweeps(self) -> "int":
        return _xbart_cpp_.XBARTcpp_get_N_sweeps(self)

    def get_burnin(self) -> "int":
        return _xbart_cpp_.XBARTcpp_get_burnin(self)

    def get_yhats(self, size: 'int') -> "void":
        return _xbart_cpp_.XBARTcpp_get_yhats(self, size)

    def get_yhats_test(self, size: 'int') -> "void":
        return _xbart_cpp_.XBARTcpp_get_yhats_test(self, size)

    def get_sigma_draw(self, size: 'int') -> "void":
        return _xbart_cpp_.XBARTcpp_get_sigma_draw(self, size)

    def get_importance(self, size: 'int') -> "void":
        return _xbart_cpp_.XBARTcpp_get_importance(self, size)

    def test_random_generator(self) -> "void":
        return _xbart_cpp_.XBARTcpp_test_random_generator(self)

    def fit_predict(self,x,y,x_test,p_cat=0):
        x_pred = self._fit_predict(x,y,x_test,y.shape[0],p_cat)
        yhats_test = self.get_yhats_test(self.get_N_sweeps()*x_test.shape[0]).reshape((x_test.shape[0],self.get_N_sweeps()),order='C')

    #self.importance = self.get_importance(x.shape[1])
        return yhats_test


    def predict(self,x_test):
        x_pred = self._predict(x_test)
        yhats_test = self.get_yhats_test(self.get_N_sweeps()*x_test.shape[0])
        yhats_test = yhats_test.reshape((x_test.shape[0],self.get_N_sweeps()),order='C')
        return yhats_test


    def fit(self,x,y,p_cat=0):
        return self._fit(x,y,p_cat)

    __swig_destroy__ = _xbart_cpp_.delete_XBARTcpp
    __del__ = lambda self: None
XBARTcpp_swigregister = _xbart_cpp_.XBARTcpp_swigregister
XBARTcpp_swigregister(XBARTcpp)

# This file is compatible with both classic and new-style classes.


