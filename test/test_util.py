# Copyright (C) 2022 Matt Langston. All Rights Reserved.
"""Unit test for the fractal_governance.util module"""

import unittest

import fractal_governance.util
import pandas as pd
from fractal_governance.util import (
    DATA_DIR,
    GENESIS_ACCOUNT_STATUS_CSV_PATH,
    GENESIS_LATE_CONSENSUS_CSV_PATH,
    GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH,
)


class TestUtil(unittest.TestCase):
    """Test fixture for the fractal_governance.util module"""

    def test_read_csv(self) -> None:
        # Adjust the paths for the bazel sandbox.
        weekly_measurements_file_path = (
            GENESIS_WEEKLY_MEASUREMENTS_CSV_PATH.relative_to(DATA_DIR)
        )
        account_status_file_path = GENESIS_ACCOUNT_STATUS_CSV_PATH.relative_to(DATA_DIR)
        late_consensus_file_path = GENESIS_LATE_CONSENSUS_CSV_PATH.relative_to(DATA_DIR)
        df = fractal_governance.util.read_csv(
            weekly_measurements_file_path=weekly_measurements_file_path,
            account_status_file_path=account_status_file_path,
            late_consensus_file_path=late_consensus_file_path,
        )
        self.assertIsNotNone(df)
        self.assertFalse(df.empty)

    def test_meeting_id_to_timestamp(self) -> None:
        self.assertEqual(
            pd.Timestamp("2022-02-26"),
            fractal_governance.util.meeting_id_to_timestamp(1),
        )
        with self.assertRaises(ValueError):
            fractal_governance.util.meeting_id_to_timestamp(0)


if __name__ == "__main__":
    unittest.main()
