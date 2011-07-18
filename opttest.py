import core
import examples
import opt

import numpy
import unittest

class TestSLSQP(unittest.TestCase):
    def test_rosenbrock_two_parameters(self):
        p = core.Project()
        p.add_parameter('x1', 0.0, (-1.5, 2.0))
        p.add_parameter('x2', 0.0, (-0.5, 3.0))
        p.add_objective('obj')
        r = examples.Rosenbrock()
        p.set_simulation(r)
        slsqp = opt.SLSQP(p)
        hist = slsqp.run()
        self.assertAlmostEquals(r.eval(hist.Best), 0.0, places=6)

    def test_rosenbrock_three_parameters(self):
        p = core.Project()
        p.add_parameter('x1', 0.0, (-1.5, 2.0))
        p.add_parameter('x2', 0.0, (-0.5, 3.0))
        p.add_parameter('x3', 0.0, (-1.5, 3.0))
        p.add_objective('obj')
        r = examples.Rosenbrock()
        p.set_simulation(examples.Rosenbrock())
        slsqp = opt.SLSQP(p)
        hist = slsqp.run()
        self.assertAlmostEquals(r.eval(hist.Best), 0.0, places=6)

if __name__ == "__main__":
    unittest.main()


