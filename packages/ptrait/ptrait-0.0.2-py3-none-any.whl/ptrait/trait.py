

class TraitExtends():
    traitmark = "__traitmark__"

    @classmethod
    def mark(cls, target_method):
        setattr(target_method, cls.traitmark, True)
        return target_method

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
