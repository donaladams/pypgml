""" Module for Bayesian Networks. """

class BayesianNetwork(object):

    def __init__(self, variables, factors, edges):
        self.variables = variables
        self.factors = factors
        self.graph = self.build_graph(variables, edges)

    def build_graph(self, variables, edges):
        pass

    def query(self, vars):
        pass


