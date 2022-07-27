# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.plots module"""

import unittest

import fractal_governance.dataset
import fractal_governance.plots
import fractal_governance.util


class TestPlots(unittest.TestCase):
    """Test fixture for the fractal_governance.plots module"""

    def test_for_smoke(self) -> None:
        # Adjust the paths for the bazel sandbox.
        fractal_dataset_csv_paths = (
            fractal_governance.util.FractalDatasetCSVPaths.relative_to(
                fractal_governance.util.DATA_DIR
            )
        )
        dataset = fractal_governance.dataset.Dataset.from_csv(fractal_dataset_csv_paths)
        self.assertIsNotNone(dataset)
        plots = fractal_governance.plots.Plots.from_dataset(dataset)
        self.assertIsNotNone(plots.dataset)
        self.assertIsNotNone(plots.attendance_vs_time)
        self.assertIsNotNone(plots.accumulated_member_respect_vs_time)
        self.assertIsNotNone(plots.accumulated_team_respect_vs_time)
        self.assertIsNotNone(plots.attendance_count_vs_level)


if __name__ == "__main__":
    unittest.main()
