import core
import examples

import numpy
import unittest

class TestRosenbrock(unittest.TestCase):
    def test_rosenbrock(self):
        r = examples.Rosenbrock()
        self.assertEquals(r.eval([0.0, 0.0])[0], 1.0, "Evaluation of two parameter Rosenbrock where both inputs are 0")
        self.assertEquals(r.eval([1.0, 1.0])[0], 0.0, "Evaluation of two parameter Rosenbrock where both inputs are 1")

if __name__ == "__main__":
    unittest.main()


