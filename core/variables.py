""" Module for random variables. """

class DiscreteRandomVariable(object):

    def __init__(self, name, domain_size, value_names=None):
        self.name = name
        self.domain_size = domain_size
        self.value_names = value_names
        self.observed_value = None

    def observe(self, value):
        if value >= 0 and value < self.domain_size:
            self.observed_value = value
        else:
            raise ValueError(
                "Value must be in [0...{0}]".format(self.domain_size-1))

    def domain(self):
        for i in xrange(self.domain_size):
            yield i

    def __cmp__(self, other):
        return cmp(self.name, other.name)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __unicode__(self):
        return u"Name:{0} Size:{1} Value:{2}".format(
            self.name, self.domain_size, self.observed_value)

    def __str__(self):
        return unicode(self).encode('utf-8')
