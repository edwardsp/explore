import core

import exceptions
import scipy.optimize

class History:
    def __init__(self, project):
        self.Project = project
        self.Count = 0
        self.Data = []
        self.Best = None

    def add_experiment(self, data):
        self.Data.append([self.Count] + data)
        self.Count += 1

    def set_best(self, best):
        self.Best = best

class Optimiser:
    def set_project(self, project):
        self.Project = project
        self.History = None

    def eval(self, x, *args):
        result = self.Project.evaluate(x, args)
        self.History.add_experiment(x + [result])
        return result

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
