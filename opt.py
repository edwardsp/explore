import core

import exceptions
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

    def eval(self, x, *args):
        result = self.History.find(x)
        if result == None:
            result = self.Project.evaluate(x)
            self.History.add_experiment(x, result)
        return result[0]

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
        best = scipy.optimize.fmin_slsqp(self.eval, start_values, bounds=bounds, iprint=0)
        return best
