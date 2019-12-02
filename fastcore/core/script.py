#AUTOGENERATED! DO NOT EDIT! File to edit: dev/05_script.ipynb (unless otherwise specified).

__all__ = ['Param', 'anno_parser', 'call_parse']

#Cell
from fastai2.core.foundation import *
from fastai2.core.utils import *
from fastai2.core.imports import *
from fastai2.test import *

from argparse import ArgumentParser

#Cell
def _param_pre(self): return '--' if self.opt else ''
def _param_kwargs(self): return {k:v for k,v in self.__dict__.items() if v is not None and k!='opt'}

#Cell
mk_class('Param', help=None, type=None, opt=True, action=None, nargs=None, const=None, choices=None, required=None,
         pre=property(_param_pre), kwargs=property(_param_kwargs),
         doc="A parameter in a function used in `anno_parser` or `call_parse`")

#Cell
def anno_parser(func):
    "Look at params (annotated with `Param`) in func and return an `ArgumentParser`"
    p = ArgumentParser(description=func.__doc__)
    for k,v in inspect.signature(func).parameters.items():
        param = func.__annotations__.get(k, Param())
        kwargs = param.kwargs
        if v.default != inspect.Parameter.empty: kwargs['default'] = v.default
        p.add_argument(f"{param.pre}{k}", **kwargs)
    return p

#Cell
def call_parse(func):
    "Decorator to create a simple CLI from `func` using `anno_parser`"
    name = inspect.currentframe().f_back.f_globals['__name__']
    if name == "__main__":
        args = anno_parser(func).parse_args()
        func(**args.__dict__)
    else: return func