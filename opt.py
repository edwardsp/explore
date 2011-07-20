import core

import exceptions
import numpy
import scipy.optimize

class History:
    def __init__(self, project):
        self.Project = project
        self.Data = []
        self.Best = None
        self.ParametersRun = {}

    def add_experiment(self, params, obj):
        self.ParametersRun[tuple(params)] = obj
        self.Data.append(list(params) + list(obj))

    def set_best(self, best):
        self.Best = best

    def find(self, params):
        p = tuple(params)
        data = None
        if p in self.ParametersRun:
            data = self.ParametersRun[p]
        return data

class Optimiser:
    def set_project(self, project):
        self.Project = project
        self.History = None

    def eval(self, x):
        result = self.History.find(x)
        if result == None:
            result = self.Project.evaluate(x)
            self.History.add_experiment(x, result)
        return result

    def obj_func(self, x, *args):
        obj = self.eval(x)
        return sum(numpy.array(obj) * numpy.array(self.Project.get_objective_weights()))

    def cons_func(self, x, *args):
        result = []
        obj = self.eval(x)
        obj_bounds = self.Project.get_objective_bounds()
        for i, b in enumerate(obj_bounds):
            if b[0] != None:
                result.append(obj[i] - b[0])
            if b[1] != None:
                result.append(-(obj[i] - b[1]))
        return numpy.array(result)

    def run(self):
        self.History = History(self.Project)
        best = self.optimise(self.Project.get_parameter_default_values(), self.Project.get_parameter_ranges())
        self.History.set_best(best)
        return self.History

    def optimise(self):
        raise exceptions.NotImplementedError()

class SLSQP(Optimiser):
    def __init__(self, project):
        self.set_project(project)

    def optimise(self, start_values, bounds):
        best = []
        if self.Project.has_constraints():
            best = scipy.optimize.fmin_slsqp(self.obj_func, start_values, f_ieqcons=self.cons_func, bounds=bounds, iprint=0)
        else:
            best = scipy.optimize.fmin_slsqp(self.obj_func, start_values, bounds=bounds, iprint=0)
        return best
