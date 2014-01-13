"""" Module defining factors and operations on factors. """

from itertools import product
from copy import deepcopy

def create_empty_table_for_factor(variables):
    sizes = [i.domain() for i in variables]
    keys =  product(*sizes)
    return {x: 0.0 for x in keys}


class Factor(object):
    """ Represents a factor over a set of random variables. """

    def __init__(self, scope, parameters=None):
        self.scope = tuple(sorted(scope))
        self.name_to_index = {
            tup[1]:tup[0] for tup in
            enumerate([x.name for x in self.scope])
        }
        self.parameters = parameters
        self.evidence = []

    def value_of_assignment(self, assignment):
        """ Return the value of an assignment in the factor. """
        if type(assignment) is not tuple:
            raise TypeError("Assignment should be of type tuple. ")
        if len(assignment) != len(self.scope):
            raise ValueError("Assignment must be same size as scope. ")

        return self.parameters[assignment]


    def sum(self, names, normalise=False):
        """ Produces a new factor by marginalising the
            named variables out of the current factor"""
        if len(names) == 0:
            return self

        # get vars that will be in resulting factor
        surviving = [
            deepcopy(s) for s in self.scope if s.name not in names
            ]

        # create resulting factor
        f = Factor(surviving)

        # perform marginalisation
        indices = [self.name_to_index[key] for key in f.names()]
        new_params = create_empty_table_for_factor(f.scope)
        denom = 0
        for assignment in self.assignment_iterator():
            new_params_key = tuple([assignment[i] for i in indices])
            new_params[new_params_key] += self.parameters[assignment]

        # set params on new factor
        f.parameters = new_params

        # normalise if required
        if normalise:
           f.normalise()

        return f

    def normalise(self):
        """ Normalises the parameters. """
        denom = sum(self.parameters.values())
        if denom > 0:
            for key in self.parameters.keys():
                self.parameters[key] /= denom

    def incorporate_evidence(self, evidence, normalise=False):
        """ Record the observed evidence and set
            incompatible assigments to p(ass) = 0 """

        def match(tup):
            return bool(tup[0] == tup[1] or tup[1] == None)

        def build_match_pattern(size, indices, evidence):
            match = [None for i in range(size)]
            for i in xrange(len(indices)):
                match[indices[i]] = evidence[i][1]
            return tuple(match)

        def assignments_match(assignment, pattern):
            tups = zip(assignment, pattern)
            return all([match(t) for t in tups])

        indices = [self.name_to_index[x[0]] for x in evidence]

        # record evidence
        self.evidence.extend(evidence)
        for i in xrange(len(indices)):
            value = evidence[i][1]
            self.scope[i].observe(value)

        # set incompatible assignments to prob of 0
        size = len(self.scope)
        match_pattern = build_match_pattern(size, indices, evidence)
        for assignment in self.assignment_iterator():
            if not(assignments_match(assignment, match_pattern)):
                self.parameters[assignment] = 0.0

        if normalise:
            self.normalise()

    def product(self, other):
        """ Produces a new factor that is the factor
            product of self and other. """

        def get_corresponding_assignment(big_factor, big_assignment, small_factor):
            """ Extract the smaller_factor's assignment that corresponds to
                the assignment of the bigger factor. """
            small_names = small_factor.names()
            small_indices = [big_factor.name_to_index[name] for name in small_names]
            return tuple([big_assignment[i] for i in small_indices])

        # get the set of all variables
        all_vars = set(self.scope).union(set(other.scope))

        # create the new Factor
        new_factor = Factor(list(all_vars))

        # create the parameter structure and assign
        params = create_empty_table_for_factor(new_factor.scope)
        new_factor.parameters = params

        # perform the product
        my_names = self.names()
        other_names = other.names()
        for assignment in new_factor.assignment_iterator():
            # build assignment key for mine
            my_assignment = get_corresponding_assignment(new_factor, assignment, self)
            # build assignment key for other
            other_assignment = get_corresponding_assignment(new_factor, assignment, other)
            # multiply
            value = self.parameters[my_assignment] * other.parameters[other_assignment]
            # assign
            new_factor.parameters[assignment] = value

        return new_factor

    def assignment_iterator(self):
        """ Iterator over the possible assignments in
            this factor. """
        sizes = [i.domain() for i in self.scope]
        return product(*sizes)

    def names(self):
        """ Return the names of variables in the
            factor's scope in order """
        return [x.name for x in self.scope]

