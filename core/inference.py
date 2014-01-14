""" Module for any inference algorithms. """
from copy import deepcopy

class VariableElimination(object):
    """ Implements the Variable Elimination algorithm
        for a set of factors. """
    def __init__(self, variables, factors):
        self.variables = deepcopy(variables)
        self.factors = set(factors)

    def query(self, names, evidence=None):

        print "\nquery({0} | {1})".format(names, evidence)
        # get the variables to be eliminated
        to_eliminate = self.get_complement_of_vars_by_name(names)

        # incorporate evidence if necessary
        self.incorporate_evidence(evidence)

        # run variable elimination:
        return self.sum_product_ve(to_eliminate)

    def incorporate_evidence(self, evidence):
        """ Add evidence in form [("name", value)...] to the factors."""
        if evidence:
            ev_size = len(evidence)
            #get variables associated with evidence
            evidence_vars = self.get_vars_by_name([x[0] for x in evidence])

            # collect all evidence pertaining to a given factor
            factor_to_evidence = {}
            for i in xrange(ev_size):
                evidence_var = evidence_vars[i]
                factors = self.get_related_factors(self.factors, evidence_var)
                for f in factors:
                    if f not in factor_to_evidence:
                        factor_to_evidence[f] = []
                    factor_to_evidence[f].append(evidence[i])

            # apply collected evidence to each factor
            for factor, ev in factor_to_evidence.items():
                factor.incorporate_evidence(ev)

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


    def get_vars_by_name(self, names):
        return [
            v for v in self.variables if v.name in names
            ]

    def get_complement_of_vars_by_name(self, names):
        return [
            v for v in self.variables if v.name not in names
            ]

