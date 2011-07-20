import core

import exceptions
import numpy
import scipy.optimize

class Optimiser:
    def obj_func(self, x, *args):
        obj = self.Simulation.evaluate(x, self.History)
        return sum(numpy.array(obj) * numpy.array(self.Project.get_objective_weights()))

    def cons_func(self, x, *args):
        result = []
        obj = self.Simulation.evaluate(x, self.History)
        obj_bounds = self.Project.get_objective_bounds()
        for i, b in enumerate(obj_bounds):
            if b[0] != None:
                result.append(obj[i] - b[0])
            if b[1] != None:
                result.append(-(obj[i] - b[1]))
        return numpy.array(result)

    def run(self, project, simulation, history=core.History()):
        self.Project = project
        self.Simulation = simulation
        self.History = history
        best = self.optimise(self.Project.get_parameter_default_values(), self.Project.get_parameter_ranges())
        self.History.set_best(best)
        return self.History

    def optimise(self):
        raise exceptions.NotImplementedError()

class SLSQP(Optimiser):
    def optimise(self, start_values, bounds):
        best = []
        if self.Project.has_constraints():
            best = scipy.optimize.fmin_slsqp(self.obj_func, start_values, f_ieqcons=self.cons_func, bounds=bounds, iprint=0)
        else:
            best = scipy.optimize.fmin_slsqp(self.obj_func, start_values, bounds=bounds, iprint=0)
        return best
