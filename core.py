
import exceptions
import json

class DefaultValueOutOfRange(exceptions.Exception):
    pass

class Simulation:
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
        self.Simulation = None

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

    def set_simulation(self, simulation):
        self.Simulation = simulation

    def evaluate(self, x):
        if (self.Simulation == None):
            raise exceptions.NotImplementedError()
        return self.Simulation.eval(x)

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
