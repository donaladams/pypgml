""" Tests for factors.py """

import nose
import random
from core.factors import create_empty_table_for_factor
from core.factors import Factor
from core.variables import DiscreteRandomVariable

class TestFactor(object):

    def test_creation(self):
        x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
        x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))

        params = {
            (0, 1): .2,
            (1, 2): 0.3,
            (0, 0): 0.1,
            (0, 2): 0.4,
            (1, 3): 0.3,
            (1, 0): 0.1,
            (0, 3): 0.3,
            (1, 1): 0.2
        }

        for key in params.keys():
            params[key] = random.random()
        f = Factor([x1, x2], params)

        assert params


    def test_sum_nothing(self):
        x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
        x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))

        params = {
            (0, 1): .2,
            (1, 2): 0.3,
            (0, 0): 0.1,
            (0, 2): 0.4,
            (1, 3): 0.3,
            (1, 0): 0.1,
            (0, 3): 0.3,
            (1, 1): 0.2
        }


        factor = Factor([x1, x2], params)
        result = factor.sum([])
        assert result == factor

    def test_sum_x1(self):
        x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
        x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))

        params = {
            (0, 1): .2,
            (1, 2): 0.3,
            (0, 0): 0.1,
            (0, 2): 0.4,
            (1, 3): 0.3,
            (1, 0): 0.1,
            (0, 3): 0.3,
            (1, 1): 0.2
        }

        factor = Factor([x1, x2], params)
        result = factor.sum([x1.name], normalise=True)
        print result.parameters

        names = result.names()
        assert len(names) == 1
        assert names[0] == 'HairColour'

    def test_sum_x1_x2(self):
        x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
        x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))

        params = {
            (0, 1): .2,
            (1, 2): 0.3,
            (0, 0): 0.1,
            (0, 2): 0.4,
            (1, 3): 0.3,
            (1, 0): 0.1,
            (0, 3): 0.3,
            (1, 1): 0.2
        }

        factor = Factor([x1, x2], params)
        result = factor.sum([x1.name, x2.name], normalise=True)
        print result.parameters
        assert result.parameters.values()[0] == 1.0

    def test_sum_x1_x2_leaving_x3(self):
        x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
        x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))
        x3 = DiscreteRandomVariable("IsDyed", 2, ('False','True'))

        params = {
            (0, 0, 0): 0.05,
            (0, 1, 0): 0.1,
            (0, 2, 0): 0.2,
            (0, 3, 0): 0.15,
            (1, 0, 0): 0.05,
            (1, 1, 0): 0.1,
            (1, 2, 0): 0.15,
            (1, 3, 0): 0.15,
            (0, 0, 1): 0.15,
            (0, 1, 1): 0.15,
            (0, 2, 1): 0.1,
            (0, 3, 1): 0.05,
            (1, 0, 1): 0.15,
            (1, 1, 1): 0.2,
            (1, 2, 1): 0.1,
            (1, 3, 1): 0.05,
        }

        factor = Factor([x1, x2, x3], params)
        result = factor.sum([x1.name, x2.name], normalise=True)
        print result.parameters
        assert all([x == 0.5 for x in result.parameters.values()])

    def test_incorporate_evidence(self):
        x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
        x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))

        params = {
            (0, 1): .2,
            (1, 2): 0.3,
            (0, 0): 0.1,
            (0, 2): 0.4,
            (1, 3): 0.3,
            (1, 0): 0.1,
            (0, 3): 0.3,
            (1, 1): 0.2
        }

        factor = Factor([x1, x2], params)
        factor.incorporate_evidence([('Gender', 0)], normalise=True)
        print factor.parameters

        for ass in factor.assignment_iterator():
            if ass[0] == 1:
                assert factor.parameters[ass] == 0


    def test_evidence_and_sum(self):
        x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
        x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))
        x3 = DiscreteRandomVariable("IsDyed", 2, ('False','True'))

        params = {
            (0, 0, 0): 0.05,
            (0, 1, 0): 0.1,
            (0, 2, 0): 0.2,
            (0, 3, 0): 0.15,
            (1, 0, 0): 0.05,
            (1, 1, 0): 0.1,
            (1, 2, 0): 0.15,
            (1, 3, 0): 0.15,
            (0, 0, 1): 0.15,
            (0, 1, 1): 0.15,
            (0, 2, 1): 0.1,
            (0, 3, 1): 0.05,
            (1, 0, 1): 0.15,
            (1, 1, 1): 0.2,
            (1, 2, 1): 0.1,
            (1, 3, 1): 0.05,
        }

        factor = Factor([x1, x2, x3], params)
        factor.incorporate_evidence([('Gender', 0)], normalise=True)
        result = factor.sum([x2.name, x3.name], normalise=True)
        print result.parameters
        # p(Gender=0) == 1
        assert result.parameters[(0,)] == 1.0


    def test_product(self):
        x1 = DiscreteRandomVariable("Gender", 2, ('Male', 'Female'))
        x2 = DiscreteRandomVariable("HairColour", 4, ('Red', 'Blonde', 'Brown', 'Black'))

        params_one = {
            (0, 1): .2,
            (1, 2): 0.3,
            (0, 0): 0.1,
            (0, 2): 0.4,
            (1, 3): 0.3,
            (1, 0): 0.1,
            (0, 3): 0.3,
            (1, 1): 0.2
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

        product = factor_one.product(factor_two)
        assert product.value_of_assignment((1,1,1)) == params_one[(1,1)] * params_two[(1,1)]





