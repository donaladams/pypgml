""" Module for any inference algorithms. """
from copy import deepcopy

class VariableElimination(object):

    def __init__(self, variables, factors):
        self.variables = variables
        self.factors = set(factors)

    def query(self, names):
        pass

    def sum_product_ve(self, to_eliminate):
        """ Main loop of variable elimination algorithm. """
        phi = deepcopy(self.factors)
        for var in to_eliminate:
            phi = self.sum_product_eliminate_var(phi, var)
        phi_star = self.reduce_factors(phi)

        return phi_star

    def sum_product_eliminate_var(self, factors, var):
        """ Eliminate single var and return unrelated_factors
            + new combined factor. """

        print
        print "----------------------------"
        print "Removing var {0}".format(var.name)
        related_factors = self.get_related_factors(factors, var)
        print "related_factors", [str(x) for x in related_factors]
        unrelated_factors = factors.difference(related_factors)
        print "unrelated_factors", [str(x) for x in unrelated_factors]
        combined_related_factors = self.reduce_factors(related_factors)
        print "combined_related_factors", str(combined_related_factors)
        new_factor = combined_related_factors.sum([var.name])
        print "new_factor", new_factor
        print new_factor.parameters
        unrelated_factors.add(new_factor)

        return unrelated_factors

    def get_related_factors(self, factors, var):
        """ Return factors that contain a given var, if any. """
        return set([factor for factor in factors if var in factor.scope])

    def reduce_factors(self, factors):
        """ Reduces a list of factors by applying factor.product(other)
            repeatedly """
        return reduce(lambda x,y: x.product(y), factors)
