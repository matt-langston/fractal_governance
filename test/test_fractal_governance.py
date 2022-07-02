# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance module"""

import unittest
from typing import List, Type

import test_dataset
import test_math
import test_plots
import test_statistics
import test_util

if __name__ == "__main__":
    test_cases_to_run: List[Type[unittest.TestCase]] = []
    test_cases_to_run.append(test_dataset.TestDataset)
    test_cases_to_run.append(test_math.TestMath)
    test_cases_to_run.append(test_plots.TestPlots)
    test_cases_to_run.append(test_statistics.TestStatistics)
    test_cases_to_run.append(test_util.TestUtil)

    test_loader = unittest.TestLoader()
    test_suite_list = []
    for test_case in test_cases_to_run:
        test_suite = test_loader.loadTestsFromTestCase(test_case)
        test_suite_list.append(test_suite)
    test_suite = unittest.TestSuite(test_suite_list)

    test_runner = unittest.TextTestRunner()
    test_results = test_runner.run(test_suite)
