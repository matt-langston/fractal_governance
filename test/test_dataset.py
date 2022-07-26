# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.dataset module"""

import unittest

import fractal_governance.dataset
from fractal_governance.util import (
    DATA_DIR,
    GENESIS_ACCOUNT_STATUS_CSV_PATH,
    GENESIS_LATE_CONSENSUS_CSV_PATH,
    GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH,
)


class TestDataset(unittest.TestCase):
    """Test fixture for the fractal_governance.dataset module"""

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
        self.assertIsNotNone(dataset.df)
        self.assertIsNotNone(dataset.df_member_summary_stats_by_member_id)
        self.assertIsNotNone(dataset.df_member_level_by_attendance_count)
        self.assertIsNotNone(dataset.df_member_respect_new_and_returning_by_meeting)
        self.assertIsNotNone(dataset.df_member_attendance_new_and_returning_by_meeting)
        self.assertIsNotNone(dataset.df_member_leader_board)
        self.assertIsNotNone(dataset.df_team_respect_by_meeting_date)
        self.assertIsNotNone(dataset.df_team_representation_by_date)
        self.assertIsNotNone(dataset.df_team_leader_board)
        self.assertGreater(dataset.total_respect, 0)
        self.assertGreater(dataset.total_member_respect, 0)
        self.assertGreater(dataset.total_team_respect, 0)
        self.assertGreater(dataset.total_unique_members, 0)
        self.assertGreater(dataset.total_meetings, 0)
        self.assertIsNotNone(dataset.last_meeting_date)
        self.assertIsNotNone(dataset.attendance_stats)
        self.assertGreater(dataset.attendance_stats.mean, 0)
        self.assertGreater(dataset.attendance_stats.standard_deviation, 0)
        self.assertIsNotNone(dataset.attendance_consistency_stats)
        self.assertGreater(dataset.attendance_consistency_stats.mean, 0)
        self.assertGreater(dataset.attendance_consistency_stats.standard_deviation, 0)
        self.assertIsNotNone(dataset.team_representation_stats)
        self.assertGreater(dataset.team_representation_stats.mean, 0)
        self.assertGreater(dataset.team_representation_stats.standard_deviation, 0)
        self.assertIsNotNone(dataset.get_returning_member_dataframe_for_meeting_id(1))


if __name__ == "__main__":
    unittest.main()
