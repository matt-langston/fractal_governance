# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.statistics module"""

import unittest
from pathlib import Path

import fractal_governance.dataset
import fractal_governance.statistics
from fractal_governance.dataset import ATTENDANCE_COUNT_COLUMN_NAME


class TestStatistics(unittest.TestCase):
    """Test fixture for the fractal_governance.statistics module"""

    def test_combined_mean(self) -> None:
        dataset = fractal_governance.dataset.Dataset.from_csv(
            Path("data/genesis-weekly_measurements.csv")
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
