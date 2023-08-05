from ptrait import TraitWith


def test_traitwith():
    class Intf:

        @classmethod
        @TraitWith.mark
        def a_classmethod(cls, a):
            return a

        @staticmethod
        @TraitWith.mark
        def a_staticmethod(a):
            return a

        @TraitWith.mark
        def a_instancemethod(self, a):
            return a

    @TraitWith.define(Intf)
    class A:
        pass
    a = A()
    assert A.a_staticmethod(1) == 1
    assert A.a_classmethod(1) == 1
    assert a.a_instancemethod(1) == 1
