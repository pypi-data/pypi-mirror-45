from ptrait import TraitExtends


def test_mark_override():
    class IntfA:

        @classmethod
        @TraitExtends.mark
        def a_classmethodA(cls, a):
            return a

        @classmethod
        @TraitExtends.mark
        def a_classmethodC(cls, a):
            return a

        @staticmethod
        @TraitExtends.mark
        def a_staticmethodA(a):
            return a

        @staticmethod
        @TraitExtends.mark
        def a_staticmethodC(a):
            return a

        @TraitExtends.mark
        def a_instancemethodA(self, a):
            return a

        @TraitExtends.mark
        def a_instancemethodC(self, a):
            return a

    class IntfB:

        @classmethod
        @TraitExtends.mark
        def a_classmethodB(cls, a):
            return a+1

        @classmethod
        @TraitExtends.mark
        def a_classmethodC(cls, a):
            return a+2

        @staticmethod
        @TraitExtends.mark
        def a_staticmethodB(a):
            return a+1

        @staticmethod
        @TraitExtends.mark
        def a_staticmethodC(a):
            return a+2

        @TraitExtends.mark
        def a_instancemethodB(self, a):
            return a+1

        @TraitExtends.mark
        def a_instancemethodC(self, a):
            return a+2

    @TraitExtends.override(IntfA, IntfB)
    class A:
        pass

    a = A()

    assert A.a_staticmethodA(1) == 1
    assert A.a_staticmethodB(1) == 2
    assert A.a_staticmethodC(1) == 3

    assert A.a_classmethodA(1) == 1
    assert A.a_classmethodB(1) == 2
    assert A.a_classmethodC(1) == 3

    assert a.a_instancemethodA(1) == 1
    assert a.a_instancemethodB(1) == 2
    assert a.a_instancemethodC(1) == 3
