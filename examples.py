import core

import numpy

class Rosenbrock(core.Simulation):
    def eval(self, x):
        d = numpy.array(x)
        return [[], [sum((1-d[:-1])**2 + 100*(d[1:] - d[:-1]**2)**2)]]
