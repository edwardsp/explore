import numpy
import unittest

import core
import doe

class TestLatinHypercube(unittest.TestCase):
    def setUp(self):
        p = core.Project()
        p.add_parameter("var1", 0.5, (0, 1))
        p.add_parameter("var2", 0.5, (0, 1))
        p.add_parameter("var3", 0.5, (0, 1))
        self.Project = p

    def tearDown(self):
        self.Project = None

    def test_sample_points_in_range(self):
        lh = doe.LatinHypercube(self.Project)
        lh.set_seed(1)
        data = lh.generate(10)
        params = self.Project.Parameters;
        for i in data:
            for p in range(len(params)):
                self.assertTrue(i[p] >= params[p].Range[0], "Parameter " + str(p) + " less than range")
                self.assertTrue(i[p] <= params[p].Range[1], "Parameter " + str(p) + " greater than range")

    def test_sample_distribution(self):
        lh = doe.LatinHypercube(self.Project)
        lh.set_seed(1)
        npts = 10
        data = lh.generate(npts)
        params = self.Project.Parameters
        for p in range(len(params)):
            high = numpy.linspace(params[p].Range[0], params[p].Range[1], npts+1)[1:]
            hits = numpy.zeros(npts)
            for pdata in data:
                hits[high.searchsorted(pdata[p])] += 1
            for i in hits:
                self.assertTrue(i == 1, "Unevenly distributed values for parameter " + str(p))

if __name__ == "__main__":
    unittest.main()
