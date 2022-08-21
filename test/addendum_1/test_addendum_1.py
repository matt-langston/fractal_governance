# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.addendum_1 module"""

import unittest
from typing import List, Type

import test_constants
import test_weighted_means

if __name__ == "__main__":
    test_cases_to_run: List[Type[unittest.TestCase]] = []
    test_cases_to_run.append(test_weighted_means.TestWeightedMeans)
    test_cases_to_run.append(test_constants.TestAddendum1Constants)

    test_loader = unittest.TestLoader()
    test_suite_list: List[unittest.TestSuite] = []
    for test_case in test_cases_to_run:
        test_suite = test_loader.loadTestsFromTestCase(test_case)
        test_suite_list.append(test_suite)
    test_suite = unittest.TestSuite(test_suite_list)

    test_runner = unittest.TextTestRunner()
    test_results = test_runner.run(test_suite)
