import functools

from ptrait.exceptions import NamedParamsNotExist


class TraitExtends():
    traitmark = "__traitmark__"

    @classmethod
    def mark(cls, target_method):
        setattr(target_method, cls.traitmark, True)
        return target_method

    @classmethod
    def check_params(cls, _func=None, *, param_names):
        def check_params_decorator(func):
            @functools.wraps(func)
            def wrapper_check_params(*args, **kwargs):
                param_names_not_exist = [
                    x for x in param_names if x not in kwargs]
                if param_names_not_exist:
                    raise NamedParamsNotExist(
                        "Param names(%s) not exists" % ", ".join(param_names_not_exist))
                return func(*args, **kwargs)
            return wrapper_check_params
        if _func is None:
            return check_params_decorator
        else:
            return check_params_decorator(_func)

    @classmethod
    def override(cls, *traits):
        def define_decorator(target_cls):
            for tr in traits:
                for elem_name in dir(tr):
                    elem = getattr(tr, elem_name, None)
                    if getattr(elem, cls.traitmark, False):
                        setattr(target_cls, elem_name, elem)
            return target_cls
        return define_decorator
