# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.plots module"""

# builtins
import unittest

# 2nd party dependencies
import fractal_governance.dataset
import fractal_governance.plots


class TestPlots(unittest.TestCase):
    """Test fixture for the fractal_governance.plots module"""

    def test_for_smoke(self):  # pylint: disable=C0116
        dataset = fractal_governance.dataset.Dataset.from_csv(
            'data/genesis-weekly_rank.csv')
        self.assertIsNotNone(dataset)
        plots = fractal_governance.plots.Plots.from_dataset(dataset)
        self.assertIsNotNone(plots.dataset)
        self.assertIsNotNone(plots.attendance_vs_time)
        self.assertIsNotNone(plots.accumulated_member_respect_vs_time)
        self.assertIsNotNone(plots.accumulated_team_respect_vs_time)
        self.assertIsNotNone(plots.attendance_count_vs_rank)


if __name__ == '__main__':
    unittest.main()
