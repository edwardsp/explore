import core
import examples

import numpy
import unittest

class TestRosenbrock(unittest.TestCase):
    def test_rosenbrock(self):
        r = examples.Rosenbrock()
        self.assertEquals(r.eval([0.0, 0.0]), 1.0, "Evaluation of two parameter Rosenbrock where both inputs are 0")
        self.assertEquals(r.eval([1.0, 1.0]), 0.0, "Evaluation of two parameter Rosenbrock where both inputs are 1")

    def test_rosenbrock_as_simulation(self):
        p = core.Project()
        p.add_parameter('x1', 0.0, (-1.5, 2.0))
        p.add_parameter('x2', 0.0, (-0.5, 3.0))
        #p.add_parameter('x3', 0.0, (-1.5, 3.0))
        p.add_objective('obj')
        p.set_simulation(examples.Rosenbrock())
        self.assertEquals(p.evaluate(p.get_parameter_default_values()), 1.0, "Evaluation from project of two parameter Rosenbrock where both inputs are 0")

if __name__ == "__main__":
    unittest.main()


