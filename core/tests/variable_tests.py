""" Unit tests for variables.py """
import nose
from nose.tools import raises
from core.variables import DiscreteRandomVariable

class TestDiscreteRandomVariable(object):

    def test_creation(self):
        var = DiscreteRandomVariable("Gender", 3, ('Male', 'Female', 'Other'))
        assert var

    def test_observe(self):
        var = DiscreteRandomVariable("Gender", 3, ('Male', 'Female', 'Other'))
        var.observe(2)
        assert var.observed_value == 2

    @raises(ValueError)
    def test_observe_out_of_range(self):
        var = DiscreteRandomVariable("Gender", 3, ('Male', 'Female', 'Other'))
        var.observe(4)
        # shouldn't reach here
        assert False