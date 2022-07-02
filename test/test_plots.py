# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.plots module"""

import unittest
from pathlib import Path

import fractal_governance.dataset
import fractal_governance.plots


class TestPlots(unittest.TestCase):
    """Test fixture for the fractal_governance.plots module"""

    def test_for_smoke(self) -> None:
        dataset = fractal_governance.dataset.Dataset.from_csv(
            Path("data/genesis-weekly_measurements.csv")
        )
        self.assertIsNotNone(dataset)
        plots = fractal_governance.plots.Plots.from_dataset(dataset)
        self.assertIsNotNone(plots.dataset)
        self.assertIsNotNone(plots.attendance_vs_time)
        self.assertIsNotNone(plots.accumulated_member_respect_vs_time)
        self.assertIsNotNone(plots.accumulated_team_respect_vs_time)
        self.assertIsNotNone(plots.attendance_count_vs_level)


if __name__ == "__main__":
    unittest.main()
