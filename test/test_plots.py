# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.plots module"""

import unittest

import fractal_governance.dataset
import fractal_governance.plots
from fractal_governance.util import (
    DATA_DIR,
    GENESIS_ACCOUNT_STATUS_CSV_PATH,
    GENESIS_LATE_CONSENSUS_CSV_PATH,
    GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH,
)


class TestPlots(unittest.TestCase):
    """Test fixture for the fractal_governance.plots module"""

    def test_for_smoke(self) -> None:
        # Adjust the paths for the bazel sandbox.
        weekly_measurements_file_path = (
            GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH.relative_to(DATA_DIR)
        )
        account_status_file_path = GENESIS_ACCOUNT_STATUS_CSV_PATH.relative_to(DATA_DIR)
        late_consensus_file_path = GENESIS_LATE_CONSENSUS_CSV_PATH.relative_to(DATA_DIR)
        dataset = fractal_governance.dataset.Dataset.from_csv(
            weekly_measurements_file_path=weekly_measurements_file_path,
            account_status_file_path=account_status_file_path,
            late_consensus_file_path=late_consensus_file_path,
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
