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
        self.assertAlmostEqual(r.eval(hist.Best)[0], 0.0, places=6)

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
        self.assertAlmostEqual(r.eval(hist.Best)[0], 0.0, places=6)

    def test_history_data(self):
        p = core.Project()
        p.add_parameter('x1', 0.0, (-1.5, 2.0))
        p.add_parameter('x2', 0.0, (-0.5, 3.0))
        p.add_parameter('x3', 0.0, (-1.5, 3.0))
        p.add_objective('obj')
        r = examples.Rosenbrock()
        p.set_simulation(examples.Rosenbrock())
        slsqp = opt.SLSQP(p)
        hist = slsqp.run()
        self.assertEqual(len(hist.Data[0]), 4, "incorrect number of columns in history")

    def test_optimiser_evaluations(self):
        p = core.Project()
        p.add_parameter('x1', 0.0, (-1.5, 2.0))
        p.add_parameter('x2', 0.0, (-0.5, 3.0))
        p.add_parameter('x3', 0.0, (-1.5, 3.0))
        p.add_objective('obj')
        r = examples.Rosenbrock()
        p.set_simulation(examples.Rosenbrock())
        slsqp = opt.SLSQP(p)
        hist = slsqp.run()
        data = numpy.array(hist.Data)[:,0:3]
        map = {}
        for i, row in enumerate(data):
            self.assertFalse(tuple(row) in map, "duplicate entry in history (" + str(row) + ") in row " + str(i))
            map[tuple(row)] = 1

    def test_rosenbrock_two_parameters_with_constraint(self):
        p = core.Project()
        p.add_parameter('x1', 0.0, (-1.5, 2.0))
        p.add_parameter('x2', 0.0, (-0.5, 3.0))
        p.add_objective('obj', bounds=(0.5, 0.8))
        r = examples.Rosenbrock()
        p.set_simulation(r)
        slsqp = opt.SLSQP(p)
        hist = slsqp.run()
        self.assertNotAlmostEqual(r.eval(hist.Best)[0], 0.0, places=6, msg="invalid answer with constraint on objective")
        self.assertAlmostEqual(r.eval(hist.Best)[0], 0.5, places=6)


if __name__ == "__main__":
    unittest.main()


