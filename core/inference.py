""" Module for any inference algorithms. """

class VariableElimination(object):

    def __init__(self, variables, factors):
        self.variables = variables
        self.factors = factors

    def query(self, names):
        pass
