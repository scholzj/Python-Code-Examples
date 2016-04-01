#!/usr/bin/env python

import unittest
import sys
import tests.test_PurePython
import tests.test_CppBinding
import tests.test_Proton

if __name__ == '__main__':
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromModule(tests.test_PurePython))
    suites.append(unittest.TestLoader().loadTestsFromModule(tests.test_CppBinding))
    suites.append(unittest.TestLoader().loadTestsFromModule(tests.test_Proton))
    allTests = unittest.TestSuite(suites)

    result = unittest.TextTestRunner(verbosity=2).run(allTests)
    sys.exit(result.wasSuccessful() != True)