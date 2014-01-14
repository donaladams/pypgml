import nose
from core.variables import DiscreteRandomVariable
from core.factors import Factor
from core.inference import VariableElimination


def get_test_data():
    x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
    x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))

    params_one = {
        (0, 0): 0.1,
        (0, 1): .2,
        (0, 2): 0.4,
        (0, 3): 0.3,
        (1, 0): 0.1,
        (1, 1): 0.2,
        (1, 2): 0.3,
        (1, 3): 0.3,
    }

    factor_one = Factor([x1, x2], params_one)

    x3 = DiscreteRandomVariable("IsDyed", 2, ('False','True'))

    params_two = {
        (0, 0): .80,
        (0, 1): .20,
        (1, 0): .5,
        (1, 1): .5
    }

    factor_two = Factor([x1, x3], params_two)

    return [x1, x2, x3], [factor_one, factor_two]


class TestVariableElimination(object):

    def test_run_one(self):
        variables, factors = get_test_data()

        to_eliminate = [variables[1],variables[2]]
        ve = VariableElimination(variables, factors)
        result = ve.sum_product_ve(to_eliminate)
        result.normalise()
        assert result.value_of_assignment((0,)) == 1.0/1.9
        assert result.value_of_assignment((1,)) == 0.9/1.9

    def test_run_two(self):
        variables, factors = get_test_data()
        to_eliminate = [variables[1]]
        ve = VariableElimination(variables, factors)
        result = ve.sum_product_ve(to_eliminate)
        print result
        print result.parameters
        result.normalise()
        print result.parameters



