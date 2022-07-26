# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.statistics module"""

import unittest

import fractal_governance.dataset
import fractal_governance.statistics
from fractal_governance.util import (
    ATTENDANCE_COUNT_COLUMN_NAME,
    DATA_DIR,
    GENESIS_ACCOUNT_STATUS_CSV_PATH,
    GENESIS_LATE_CONSENSUS_CSV_PATH,
    GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH,
)


class TestStatistics(unittest.TestCase):
    """Test fixture for the fractal_governance.statistics module"""

    def test_combined_mean(self) -> None:
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
        df_member_level_by_attendance_count = (
            dataset.df_member_summary_stats_by_member_id.groupby(
                ATTENDANCE_COUNT_COLUMN_NAME
            )
            .apply(fractal_governance.dataset.combined_statistics)
            .reset_index()
        )
        self.assertIsNotNone(df_member_level_by_attendance_count)


if __name__ == "__main__":
    unittest.main()
