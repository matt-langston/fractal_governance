# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.statistics module"""

# builtins
import unittest

# 2nd party dependencies
import fractal_governance.statistics
import fractal_governance.dataset

from fractal_governance.dataset import ATTENDANCE_COUNT_COLUMN_NAME


class TestStatistics(unittest.TestCase):
    """Test fixture for the fractal_governance.statistics module"""

    def test_combined_mean(self):  # pylint: disable=C0116
        dataset = fractal_governance.dataset.Dataset.from_csv(
            'data/genesis-weekly_measurements.csv')  # pylint: disable=C0103
        df_member_level_by_attendance_count = dataset.df_member_summary_stats_by_member_id.groupby(
            ATTENDANCE_COUNT_COLUMN_NAME).apply(
                fractal_governance.dataset.combined_statistics).reset_index()
        self.assertIsNotNone(df_member_level_by_attendance_count)


if __name__ == '__main__':
    unittest.main()
