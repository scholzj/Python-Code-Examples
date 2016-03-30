import unittest
import sys
import tests.test_PurePython

if __name__ == '__main__':
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromModule(tests.test_PurePython))
    allTests = unittest.TestSuite(suites)

    result = unittest.TextTestRunner(verbosity=2).run(allTests)
    sys.exit(result.wasSuccessful() != True)