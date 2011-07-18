
import exceptions
import json

class DefaultValueOutOfRange(exceptions.Exception):
    pass

class Simulation:
    pass

class Parameter:
    def __init__(self,  name='NO-NAME',  default=0.0,  range=(None, None)):
        self.Name = name
        self.Default = default
        self.Range = range
        if (range[0] and default < range[0]) or (range[1] and default > range[1]):
            raise DefaultValueOutOfRange()

class Constraint:
    def __init__(self,  name='NO-NAME',  bounds=(None, None)):
        self.Name = name
        self.Bounds = bounds

class Objective:
    def __init__(self,  name='NO-NAME'):
        self.Name = name


class Project:
    def __init__(self):
        self.Parameters	= []
        self.Constraints = []
        self.Objectives = []
        self.Simulations = None

    def add_parameter(self, name, default_value, range=(None, None)):
        self.Parameters.append(Parameter(name, default_value, range))

    def get_parameter_names(self):
        return [ p.Name for p in self.Parameters ]

    def get_parameter_default_values(self):
        return [ p.Default for p in self.Parameters ]

    def get_parameter_ranges(self):
        return [ p.Range for p in self.Parameters ]

    def add_constraint(self, name, bounds):
        self.Constraints.append(Constraint(name, bounds))

    def get_constraint_names(self):
        return [ c.Name for c in self.Constraints ]

    def get_constraint_bounds(self):
        return [ c.Bounds for c in self.Constraints ]

    def add_objective(self, name):
        self.Objectives.append(Objective(name))

    def get_objective_names(self):
        return [ o.Name for o in self.Objectives ]

    def set_simulation(self, simulation):
        self.Simulation = simulation

    def evaluate(self, x, *args):
        if (self.Simulation == None):
            raise exceptions.NotImplementedError()
        return self.Simulation.eval(x, *args)

    def from_json(self, json_str):
        data = json.loads(json_str)
        self.Parameters = [ Parameter(p['Name'], p['Default'], p['Range'])
            for p in data['Parameters'] ]
        self.Constraints = [ Constraint(c['Name'], c['Bounds'])
            for c in data['Constraints'] ]
        self.Objectives = [ Objective(o['Name']) for o in data['Objectives'] ]

    def to_json(self):
        return json.dumps({
            'Parameters': [
                { 'Name':p.Name, 'Default':p.Default, 'Range':p.Range }
                    for p in self.Parameters ],
            'Constraints': [
                { 'Name':c.Name, 'Bounds':c.Bounds }
                    for c in self.Constraints ],
            'Objectives': [
                { 'Name':p.Name } for o in self.Objectives ] })

    def open(self, filename):
        pass
