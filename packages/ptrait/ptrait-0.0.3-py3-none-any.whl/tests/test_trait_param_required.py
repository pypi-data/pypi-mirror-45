from ptrait.trait import TraitExtends
from ptrait.exceptions import NamedParamsNotExist
import pytest


class TestA:
    @TraitExtends.check_params(param_names=['abc'])
    def method_a(self, **kwargs):
        return kwargs


def test_param_required_success():
    a = TestA()
    a.method_a(abc=1)


@pytest.mark.xfail(NamedParamsNotExist)
def test_param_required_ne_error():
    a = TestA()
    a.method_a(aaa=1)
