
import exceptions
import json

class DefaultValueOutOfRange(exceptions.Exception):
    pass

class History:
    def __init__(self):
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

class Simulation:
    def run_doe(self, data, hist=History()):
        for params in data:
            hist.add_experiment(params, self.evaluate(params, hist))
        return hist

    def evaluate(self, x, hist):
        result = hist.find(x)
        if result == None:
            result = self.eval(x)
            hist.add_experiment(x, result)
        return result

    def eval(self, x):
        raise exceptions.NotImplementedException()

class Parameter:
    def __init__(self,  name='NO-NAME',  default=0.0,  range=(None, None)):
        self.Name = name
        self.Default = default
        self.Range = range
        if (range[0] and default < range[0]) or (range[1] and default > range[1]):
            raise DefaultValueOutOfRange()

class Objective:
    def __init__(self,  name='NO-NAME', bounds=(None, None), weight=1.0):
        self.Name = name
        self.Bounds = bounds
        self.Weight = weight


class Project:
    def __init__(self):
        self.Parameters	= []
        self.Objectives = []

    def add_parameter(self, name, default_value, range=(None, None)):
        self.Parameters.append(Parameter(name, default_value, range))

    def get_parameter_names(self):
        return [ p.Name for p in self.Parameters ]

    def get_parameter_default_values(self):
        return [ p.Default for p in self.Parameters ]

    def get_parameter_ranges(self):
        return [ p.Range for p in self.Parameters ]

    def add_objective(self, name, bounds=(None, None), weight=1.0):
        self.Objectives.append(Objective(name, bounds, weight))

    def get_objective_names(self):
        return [ o.Name for o in self.Objectives ]

    def get_objective_bounds(self):
        return [ o.Bounds for o in self.Objectives ]

    def get_objective_weights(self):
        return [ o.Weight for o in self.Objectives ]

    def has_constraints(self):
        result = False
        for o in self.Objectives:
            if o.Bounds != (None, None):
                result = True
        return result

    def from_json(self, json_str):
        data = json.loads(json_str)
        self.Parameters = [ Parameter(p['Name'], p['Default'], p['Range'])
            for p in data['Parameters'] ]
        self.Objectives = [ Objective(o['Name'], o['Bounds'], o['Weight'])
            for o in data['Objectives'] ]

    def to_json(self):
        return json.dumps({
            'Parameters': [
                { 'Name':p.Name, 'Default':p.Default, 'Range':p.Range }
                    for p in self.Parameters ],
            'Objectives': [
                { 'Name':o.Name, 'Bounds':o.Bounds, 'Weight':o.Weight }
                    for o in self.Objectives ] })

    def open(self, filename):
        pass
