# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.dataset module"""

# builtins
import unittest

# 2nd party dependencies
import fractal_governance.dataset


class TestDataset(unittest.TestCase):
    """Test fixture for the fractal_governance.dataset module"""

    def test_for_smoke(self):  # pylint: disable=C0116
        dataset = fractal_governance.dataset.Dataset.from_csv(
            'data/genesis-weekly_rank.csv')
        self.assertIsNotNone(dataset)
        self.assertIsNotNone(dataset.df)
        self.assertIsNotNone(dataset.df_member_summary_stats_by_member_id)
        self.assertIsNotNone(dataset.df_member_rank_by_attendance_count)
        self.assertIsNotNone(
            dataset.df_member_respect_new_and_returning_by_meeting)
        self.assertIsNotNone(
            dataset.df_member_attendance_new_and_returning_by_meeting)
        self.assertIsNotNone(dataset.df_member_leader_board)
        self.assertIsNotNone(dataset.df_team_respect_by_meeting_date)
        self.assertIsNotNone(dataset.df_team_representation_by_date)
        self.assertIsNotNone(dataset.df_team_leader_board)
        self.assertGreater(dataset.total_respect, 0)
        self.assertGreater(dataset.total_member_respect, 0)
        self.assertGreater(dataset.total_team_respect, 0)
        self.assertIsNotNone(dataset.last_meeting_date)
        self.assertIsNotNone(dataset.attendance_stats)
        self.assertGreater(dataset.attendance_stats.mean, 0)
        self.assertGreater(dataset.attendance_stats.standard_deviation, 0)
        self.assertIsNotNone(dataset.team_representation_stats)
        self.assertGreater(dataset.team_representation_stats.mean, 0)
        self.assertGreater(
            dataset.team_representation_stats.standard_deviation, 0)


if __name__ == '__main__':
    unittest.main()
