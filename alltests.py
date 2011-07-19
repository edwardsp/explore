import unittest

import coretest
import doetest
import examplestest
import opttest

if __name__ == '__main__':
    suites = [
        unittest.findTestCases(coretest),
        unittest.findTestCases(doetest),
        unittest.findTestCases(examplestest),
        unittest.findTestCases(opttest) ]

    runner = unittest.TextTestRunner()
    runner.verbosity = 2
    runner.run(unittest.TestSuite(suites))
