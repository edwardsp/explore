import core

import random

class LatinHypercube:
    def __init__(self,  project):
        self.Project = project

    def set_seed(self, n):
        random.seed(n)

    def generate(self,  n):
        plimits = [ (p.Range[0], p.Range[1], (p.Range[1] - p.Range[0])/float(n)) for p in self.Project.Parameters ]
        np = len(plimits)
        pranges = []
        for low, high, delta in plimits:
            pranges.append([ random.uniform(low + j * delta,  low + (j + 1) * delta) for j in range(n)])
        s = [range(0, n) for i in range(0, np)]

        result = []
        for i in range(0, n):
            tmp = []
            for j in range(0, np):
                a = random.sample(s[j], 1)[0]
                tmp.append(pranges[j][a])
                s[j].remove(a)
            result.append(tmp)

        return result
